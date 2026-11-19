# syntax=docker/dockerfile:1.6

# ==============================================================================
# STAGE 1: Conda-Forge Scientific & GDAL Toolchain
# ==============================================================================
FROM mambaorg/micromamba:ubuntu24.04 AS toolchain

USER root

ENV VIRTUAL_ENV=/opt/venv \
    MAMBA_ROOT_PREFIX=/opt/conda \
    MAMBA_EXTRACT_THREADS=2 \
    PATH="/opt/venv/bin:$PATH"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        fish \
        git \
        tzdata

RUN --mount=type=cache,target=/opt/conda/pkgs/cache \
    ln -sfn "$(which micromamba)" /usr/local/bin/mamba && \
    micromamba create -y -v -p /opt/venv -c conda-forge \
        python=3.12 \
        pip \
        "setuptools<81" \
        wheel \
        libgdal-netcdf \
        libgdal-hdf5 \
        "rasterio~=1.5.2" \
        pyproj \
        "shapely~=2.2.0" \
        "h5py~=3.14.0" \
        "matplotlib-base~=3.10.9" \
        "pandas~=3.1.1" \
        "scipy~=1.18.1" \
        "scikit-learn~=1.9.1" \
        "numpy~=2.5.4" && \
    micromamba clean -a -y && \
    python --version && \
    mamba --version

# ==============================================================================
# STAGE 2: Package Build & Dependencies (Installed into /opt/venv)
# ==============================================================================
FROM toolchain AS build

WORKDIR /tmp/src
COPY . /tmp/src/

RUN pip list --format=freeze | grep -E '^(numpy|scipy|rasterio|shapely|h5py|pandas|matplotlib|pyproj|scikit-learn)==' > /tmp/conda-constraints.txt && \
    pip install \
      --no-cache-dir \
      --upgrade-strategy only-if-needed \
      -c /tmp/conda-constraints.txt \
      .[dev] && \
    rm -rf /tmp/src /tmp/conda-constraints.txt

# ==============================================================================
# STAGE 3: Runtime Image
# ==============================================================================
FROM build AS runtime

ENV TZ=UTC \
    OPENBLAS_NUM_THREADS=1 \
    OMP_NUM_THREADS=1 \
    TF_CPP_MIN_LOG_LEVEL=2 \
    TF_ENABLE_ONEDNN_OPTS=0 \
    MPLCONFIGDIR=/opt/matplotlib \
    GDAL_DRIVER_PATH="/opt/venv/lib/gdalplugins" \
    GDAL_DATA="/opt/venv/share/gdal" \
    PROJ_DATA="/opt/venv/share/proj" \
    SHELL=/usr/bin/fish

RUN mkdir -p /opt/matplotlib /etc/fish && \
    chsh -s /usr/bin/fish root && \
    micromamba shell init -s fish -r /opt/conda && \
    micromamba shell init -s bash -r /opt/conda && \
    printf '\nset -gx PATH /opt/venv/bin /usr/local/bin $PATH\n' >> /etc/fish/config.fish && \
    python -c "import matplotlib.font_manager" && \
    find /opt/venv /opt/matplotlib \
        \( -type d ! -perm -a+rx -o -type f ! -perm -a+r \) \
        -exec chmod a+rX {} +

WORKDIR /root

ENTRYPOINT []
CMD ["/usr/bin/fish"]
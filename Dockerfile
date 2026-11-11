# Using Debian-based python:3.13.2-bookworm base image
FROM python:3.10.16-bookworm as base
ENV HOME /root

FROM base as environment

# Update Debian and install required dependencies
RUN apt-get update && apt-get install -y --no-install-recommends tzdata wget fish
RUN pip install --upgrade pip
RUN pip install tomli

FROM environment as installation

# Creating directory inside container to store PGE code
RUN mkdir /app

# Copying current snapshot of PGE code repository into container
COPY . /app/

# Running pip install using pyproject.toml
COPY pyproject.toml /app/pyproject.toml
WORKDIR /app

# FROM dependencies as build
FROM installation as build
RUN pip install -e .[dev]
RUN rm -rvf build; rm -rvf dist; rm -rvf *.egg-info

# Docker smoke test stage - validates package installation and environment compatibility
FROM build as smoke-test
WORKDIR /app
RUN echo "=== Running Docker Smoke Tests ===" && \
    echo "Python version: $(python --version)" && \
    echo "Package installation check..." && \
    python -c "import ECOv003_L3T_L4T_JET; print(f'✓ ECOv003_L3T_L4T_JET package imported successfully')" && \
    echo "Running smoke test..." && \
    python -c "import ECOv003_L3T_L4T_JET; ECOv003_L3T_L4T_JET.test()" && \
    echo "=== All Smoke Tests Passed ✓ ==="

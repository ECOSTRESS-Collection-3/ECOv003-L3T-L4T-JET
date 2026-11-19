# Using Debian-based python:3.12-bookworm base image
FROM python:3.12-bookworm AS base
ENV HOME=/root

FROM base AS environment

# Update Debian and install required dependencies
RUN apt-get update && apt-get install -y --no-install-recommends tzdata wget fish
RUN pip install --upgrade pip
RUN pip install tomli

FROM environment AS installation

# Creating directory inside container to store PGE code
RUN mkdir /app

# Copying current snapshot of PGE code repository into container
COPY . /app/
WORKDIR /app

FROM installation AS build
RUN pip install -e .[dev]
RUN rm -rvf build; rm -rvf dist; rm -rvf *.egg-info

# Docker smoke test stage - validates package installation and environment compatibility
FROM build AS smoke-test
WORKDIR /app
RUN echo "=== Running Docker Smoke Tests ===" &&     echo "Python version: $(python --version)" &&     echo "Package installation check..." &&     python -c "import ECOv003_L3T_L4T_JET; print('✓ ECOv003_L3T_L4T_JET package imported successfully')" &&     echo "Running smoke test..." &&     python -c "import ECOv003_L3T_L4T_JET; ECOv003_L3T_L4T_JET.test()" &&     echo "=== All Smoke Tests Passed ✓ ==="

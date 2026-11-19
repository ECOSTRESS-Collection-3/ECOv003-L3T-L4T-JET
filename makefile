# Define the package name, environment name, and Python version
PACKAGE_NAME = ECOv003-L3T-L4T-JET
MODULE_NAME = $(subst -,_,$(PACKAGE_NAME))
ENVIRONMENT_NAME = $(PACKAGE_NAME)
DOCKER_IMAGE_NAME = $(shell echo $(PACKAGE_NAME) | tr '[:upper:]' '[:lower:]')
PYTHON_VERSION = $(if $(PYTHON),$(PYTHON),3.12)

# Allow passing extra flags via command line: make <target> ARGS="--progress=plain"
ARGS ?=
DOCKER_BUILD_FLAGS ?= --platform linux/amd64 $(ARGS)
DOCKER_RUN_FLAGS ?= --platform linux/amd64

# Include a Makefile.local to override things, if found
-include Makefile.local

.PHONY: clean test verify build twine-upload dist install uninstall reinstall \
        environment remove-environment colima-start colima-reset \
        docker-build docker-build-toolchain docker-build-installation docker-build-runtime \
        docker-rebuild-toolchain docker-rebuild-installation docker-rebuild-runtime docker-rebuild-all \
        docker-interactive docker-remove docker-clean \
        compile-documentation smoke-test smoke-test-cli docker-smoke-test repomix

# Clean up build artifacts and temporary files
clean:
	rm -rf *.o *.out *.log
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

# Run tests using pytest
test:
	pytest -vv -p no:warnings

# Run the smoke test locally using the Python API
smoke-test:
	python -c "import $(MODULE_NAME); success = $(MODULE_NAME).test(); exit(0 if success else 1)"

# Run the smoke test locally via the installed CLI sub-command
smoke-test-cli:
	$(PACKAGE_NAME) test

# Verify the package installation and functionality via JET3
verify:
	python -c "from JET3 import verify; exit(0 if verify() else 1)"

# Build the Python package
build:
	python -m build

# Upload the built package to PyPI using Twine
twine-upload:
	twine upload dist/*

# Clean, build, and upload the package
dist:
	make clean
	make build
	make twine-upload

# Install the package in editable mode with development dependencies
install:
	pip install -e .[dev]

# Uninstall the package
uninstall:
	pip uninstall $(PACKAGE_NAME)

# Reinstall the package (uninstall and then install)
reinstall:
	make uninstall
	make install

# Create a new Conda environment with the specified Python version
environment:
	mamba create -y -n $(ENVIRONMENT_NAME) -c conda-forge python=$(PYTHON_VERSION)

# Remove the Conda environment
remove-environment:
	mamba env remove -y -n $(ENVIRONMENT_NAME)

# Start Colima with the required settings to prevent Rosetta 2 crashes
colima-start:
	colima start --vm-type=vz --vz-rosetta=true --cpu 6 --memory 16 --disk 100

# Completely reset the Colima VM before starting to prevent vz/qemu driver hanging issues
colima-reset:
	colima delete -f
	colima start --vm-type=vz --vz-rosetta=true --cpu 6 --memory 16 --disk 100

# Build the Docker image (final runtime stage)
docker-build: docker-build-runtime

# Build the Docker image up to the 'toolchain' target stage
docker-build-toolchain:
	DOCKER_BUILDKIT=1 docker build --target toolchain $(DOCKER_BUILD_FLAGS) -t $(DOCKER_IMAGE_NAME):toolchain .

# Build the Docker image up to the 'build' target stage
docker-build-installation:
	DOCKER_BUILDKIT=1 docker build --target build $(DOCKER_BUILD_FLAGS) -t $(DOCKER_IMAGE_NAME):build .

# Build the Docker image up to the 'runtime' target stage
docker-build-runtime:
	DOCKER_BUILDKIT=1 docker build --target runtime $(DOCKER_BUILD_FLAGS) -t $(DOCKER_IMAGE_NAME):latest .

# Build the runtime image and execute smoke tests inside a container
docker-smoke-test: docker-build-runtime
	@echo "=== Running Container Smoke Tests ==="
	docker run --rm $(DOCKER_RUN_FLAGS) $(DOCKER_IMAGE_NAME):latest python -c "import ECOv003_L3T_L4T_JET; raise SystemExit(0 if ECOv003_L3T_L4T_JET.test() else 1)"
	docker run --rm $(DOCKER_RUN_FLAGS) $(DOCKER_IMAGE_NAME):latest ECOv003-L3T-L4T-JET test
	docker run --rm $(DOCKER_RUN_FLAGS) -v "$(PWD)/tests:/tests:ro" $(DOCKER_IMAGE_NAME):latest pytest /tests/test_docker_smoke.py /tests/test_import_dependencies.py -p no:cacheprovider -p no:warnings -vv

# Granular cache-busting rebuilds (--no-cache-filter)
docker-rebuild-toolchain:
	DOCKER_BUILDKIT=1 docker build --no-cache-filter toolchain --target toolchain $(DOCKER_BUILD_FLAGS) -t $(DOCKER_IMAGE_NAME):toolchain .

docker-rebuild-installation:
	DOCKER_BUILDKIT=1 docker build --no-cache-filter build --target build $(DOCKER_BUILD_FLAGS) -t $(DOCKER_IMAGE_NAME):build .

docker-rebuild-runtime:
	DOCKER_BUILDKIT=1 docker build --no-cache-filter runtime --target runtime $(DOCKER_BUILD_FLAGS) -t $(DOCKER_IMAGE_NAME):latest .

docker-rebuild-all:
	DOCKER_BUILDKIT=1 docker build --no-cache --target runtime $(DOCKER_BUILD_FLAGS) -t $(DOCKER_IMAGE_NAME):latest .

# Run the Docker container interactively with the Fish shell
docker-interactive:
	docker run -it --rm $(DOCKER_RUN_FLAGS) $(DOCKER_IMAGE_NAME):latest /usr/bin/fish

# Remove the Docker image and stage tags
docker-remove:
	-docker rmi -f $(DOCKER_IMAGE_NAME):latest $(DOCKER_IMAGE_NAME):build $(DOCKER_IMAGE_NAME):toolchain 2>/dev/null || true

# Clean stopped containers, project images, and dangling layers
docker-clean: docker-remove
	docker image prune -f

# Compile the ATBD and User Guide from Markdown to PDF
compile-documentation:
	bash documentation/ECOv003_L3_L4_JET_ATBD.sh
	bash documentation/ECOv003_L3_L4_JET_User_Guide.sh

repomix:
	npx repomix --ignore "**/*.pdf,**/*.jpeg,**/*.dat,**/*.ipynb,**/*.tex"
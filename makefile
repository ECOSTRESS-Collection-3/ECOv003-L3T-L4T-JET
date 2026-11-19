# Define the package name, environment name, and Python version
PACKAGE_NAME = ECOv003-L3T-L4T-JET
MODULE_NAME = $(subst -,_,$(PACKAGE_NAME))
ENVIRONMENT_NAME = $(PACKAGE_NAME)
DOCKER_IMAGE_NAME = $(shell echo $(PACKAGE_NAME) | tr '[:upper:]' '[:lower:]')
PYTHON_VERSION = $(if $(PYTHON),$(PYTHON),3.12)

.PHONY: clean test verify build twine-upload dist install uninstall reinstall \
        environment remove-environment colima-start docker-build docker-build-environment \
        docker-build-installation docker-interactive docker-remove \
        compile-documentation smoke-test smoke-test-cli docker-smoke-test docker-smoke-test-skip repomix

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

# Start Colima with specific resource settings
colima-start:
	colima start -m 16 -a x86_64 -d 100

# Build the Docker image
docker-build:
	docker build -t $(DOCKER_IMAGE_NAME):latest .

# Build the Docker image up to the 'environment' target stage
docker-build-environment:
	docker build --target environment -t $(DOCKER_IMAGE_NAME):latest .

# Build the Docker image up to the 'installation' target stage
docker-build-installation:
	docker build --target installation -t $(DOCKER_IMAGE_NAME):latest .

# Build the Docker image up to the 'smoke-test' stage (runs smoke tests during build)
docker-smoke-test:
	docker build --target smoke-test -t $(DOCKER_IMAGE_NAME):latest .

# Build Docker image up to 'build' stage, skipping smoke tests
docker-smoke-test-skip:
	docker build --target build -t $(DOCKER_IMAGE_NAME):latest .

# Run the Docker container interactively with the Fish shell
docker-interactive:
	docker run -it $(DOCKER_IMAGE_NAME) fish

# Remove the Docker image
docker-remove:
	docker rmi -f $(DOCKER_IMAGE_NAME)

# Compile the ATBD and User Guide from Markdown to PDF
compile-documentation:
	bash documentation/ECOv003_L3_L4_JET_ATBD.sh
	bash documentation/ECOv003_L3_L4_JET_User_Guide.sh

repomix:
	npx repomix --ignore "**/*.pdf,**/*.jpeg,**/*.dat,**/*.ipynb,**/*.tex"

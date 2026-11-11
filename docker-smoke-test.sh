#!/usr/bin/env bash
# Docker build and smoke test helper script
# Runs the package installation and smoke tests in a Docker container

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCKER_IMAGE_NAME="${DOCKER_IMAGE_NAME:-ecov003-l3t-l4t-jet}"
DOCKER_IMAGE_TAG="${DOCKER_IMAGE_TAG:-latest}"

echo "=========================================="
echo "ECOv003-L3T-L4T-JET Docker Smoke Test"
echo "=========================================="
echo ""

# Parse arguments
SKIP_SMOKE_TEST=false
BUILD_TARGET="smoke-test"

while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-smoke-test)
            SKIP_SMOKE_TEST=true
            BUILD_TARGET="build"
            shift
            ;;
        --image-name)
            DOCKER_IMAGE_NAME="$2"
            shift 2
            ;;
        --image-tag)
            DOCKER_IMAGE_TAG="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --skip-smoke-test    Build without running smoke tests"
            echo "  --image-name NAME    Docker image name (default: $DOCKER_IMAGE_NAME)"
            echo "  --image-tag TAG      Docker image tag (default: $DOCKER_IMAGE_TAG)"
            echo "  -h, --help          Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo "Building Docker image: ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
echo "Build target: ${BUILD_TARGET}"
echo ""

cd "$SCRIPT_DIR"

# Build Docker image with the specified target
docker build \
    --target "${BUILD_TARGET}" \
    -t "${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}" \
    .

BUILD_EXIT_CODE=$?

if [ $BUILD_EXIT_CODE -eq 0 ]; then
    echo ""
    echo "=========================================="
    if [ "$SKIP_SMOKE_TEST" = false ]; then
        echo "✓ Docker image built successfully with smoke tests passing!"
    else
        echo "✓ Docker image built successfully!"
    fi
    echo "=========================================="
    echo ""
    echo "Image: ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
    echo ""
    echo "To run the container:"
    echo "  docker run -it ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} /bin/bash"
    echo ""
    exit 0
else
    echo ""
    echo "=========================================="
    echo "✗ Docker build failed!"
    echo "=========================================="
    exit $BUILD_EXIT_CODE
fi

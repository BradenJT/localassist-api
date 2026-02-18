#!/bin/bash
# scripts/build_lambda_linux.sh
# Build Lambda packages for Linux (GitHub Actions)

set -e

echo "🔨 Building Lambda packages for Linux..."

# Variables
BUILD_DIR="build"
LAYER_DIR="$BUILD_DIR/layer/python"
FUNCTION_DIR="$BUILD_DIR/function"

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf $BUILD_DIR
rm -f lambda_function.zip
rm -f lambda_layer.zip

# Create directories
mkdir -p $LAYER_DIR
mkdir -p $FUNCTION_DIR

# Install dependencies to layer (excluding dev dependencies)
echo "Installing Python dependencies for Lambda layer..."
pip install \
  fastapi==0.104.1 \
  uvicorn[standard]==0.24.0 \
  pydantic==2.4.2 \
  pydantic-settings==2.0.3 \
  python-jose[cryptography]==3.3.0 \
  passlib[bcrypt]==1.7.4 \
  bcrypt==4.1.2 \
  boto3==1.29.7 \
  python-multipart==0.0.6 \
  python-dotenv==1.0.0 \
  mangum==0.17.0 \
  -t $LAYER_DIR \
  --no-cache-dir \
  --platform manylinux2014_x86_64 \
  --only-binary=:all: \
  --upgrade

# Clean up unnecessary files to reduce size
echo "Cleaning up layer..."
cd $LAYER_DIR
find . -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
find . -type d -name "*.dist-info" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
cd ../../..

# Create layer zip
echo "Creating Lambda layer zip..."
cd $BUILD_DIR/layer
zip -r9 ../../lambda_layer.zip . -q
cd ../..

# Copy application code to function directory
echo "Copying application code..."
cp -r app $FUNCTION_DIR/

# Create function zip (without dependencies - they're in the layer)
echo "Creating Lambda function zip..."
cd $FUNCTION_DIR
zip -r9 ../../lambda_function.zip . -q
cd ../..

# Get sizes
LAYER_SIZE=$(du -h lambda_layer.zip | cut -f1)
FUNCTION_SIZE=$(du -h lambda_function.zip | cut -f1)

echo "✅ Build complete!"
echo "Lambda layer:    ${LAYER_SIZE}"
echo "Lambda function: ${FUNCTION_SIZE}"

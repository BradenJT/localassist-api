#!/bin/bash
# scripts/build_lambda.sh

set -e  # Exit on error

echo "🔨 Building Lambda package..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables
BUILD_DIR="build"
LAYER_DIR="$BUILD_DIR/layer/python"
FUNCTION_DIR="$BUILD_DIR/function"

# Clean previous builds
echo -e "${BLUE}Cleaning previous builds...${NC}"
rm -rf $BUILD_DIR
rm -f lambda_function.zip
rm -f lambda_layer.zip

# Create directories
mkdir -p $LAYER_DIR
mkdir -p $FUNCTION_DIR

# Install dependencies to layer
echo -e "${BLUE}Installing dependencies for Lambda layer...${NC}"
pip install -r requirements.txt -t $LAYER_DIR --upgrade

# Remove unnecessary files to reduce size
echo -e "${BLUE}Cleaning up layer...${NC}"
cd $BUILD_DIR/layer/python
find . -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
find . -type d -name "*.dist-info" -exec rm -rf {} + 2>/dev/null || true
cd ../../..

# Create layer zip
echo -e "${BLUE}Creating Lambda layer zip...${NC}"
cd $BUILD_DIR/layer
zip -r9 ../../lambda_layer.zip . -q
cd ../..

# Copy application code to function directory
echo -e "${BLUE}Copying application code...${NC}"
cp -r app $FUNCTION_DIR/

# Create function zip (without dependencies - they're in the layer)
echo -e "${BLUE}Creating Lambda function zip...${NC}"
cd $FUNCTION_DIR
zip -r9 ../../lambda_function.zip . -q
cd ../..

# Get sizes
LAYER_SIZE=$(du -h lambda_layer.zip | cut -f1)
FUNCTION_SIZE=$(du -h lambda_function.zip | cut -f1)

echo -e "${GREEN}✅ Build complete!${NC}"
echo -e "Lambda layer:    ${GREEN}${LAYER_SIZE}${NC}"
echo -e "Lambda function: ${GREEN}${FUNCTION_SIZE}${NC}"
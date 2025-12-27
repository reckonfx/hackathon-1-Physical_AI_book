#!/bin/bash
# Development startup script for Physical AI Book
# This script copies the dev configuration and starts the server

echo "Starting Physical AI Book in development mode..."
echo "Using development configuration with correct base URL..."

# Copy dev config to main config temporarily
cp docusaurus.config.dev.js docusaurus.config.js

# Start the development server
npx docusaurus start

echo "Server stopped. Restoring production configuration..."
# Restore the original configuration
git checkout docusaurus.config.js
@echo off
REM Development startup script for Physical AI Book (Windows)
REM This script copies the dev configuration and starts the server

echo Starting Physical AI Book in development mode...
echo Using development configuration with correct base URL...

REM Copy dev config to main config temporarily
copy docusaurus.config.dev.js docusaurus.config.js

REM Start the development server
npx docusaurus start

REM Restore the original configuration (this will run when the server is stopped)
echo Server stopped. Restoring production configuration...
git checkout docusaurus.config.js
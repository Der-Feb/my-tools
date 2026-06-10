@echo off
REM Build script for Ultimate Dev Toolbox
REM Requirements: venv activated and dependencies installed

REM Build a single .exe file
pyinstaller --onefile --name tool main.py

REM Clean up build files (keep dist and __pycache__)
rmdir /s /q build
del tool.spec

echo.
echo Done! Your executable is in the dist/ folder.
echo Copy dist/tool.exe to a location in your PATH to use it anywhere!

@echo off
REM Simple launcher for pyWebmConverter GUI on Windows
REM Usage: Double-click this file or run: run.bat

python -m pyWebmConverter %*
if errorlevel 1 (
    echo.
    echo Error: Could not start pyWebmConverter
    echo.
    echo Make sure you have:
    echo   1. Python installed and in PATH
    echo   2. Run "pip install -e ." to install the package
    echo.
    pause
)

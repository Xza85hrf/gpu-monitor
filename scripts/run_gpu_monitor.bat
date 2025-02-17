@echo off
echo Starting GPU Monitor...

:: Set project root directory
set "PROJECT_ROOT=%~dp0.."
cd /d "%PROJECT_ROOT%"

:: Add src directory to PYTHONPATH
set "PYTHONPATH=%PROJECT_ROOT%;%PYTHONPATH%"

:: Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

:: Check if virtual environment exists, if not create it
if not exist "%PROJECT_ROOT%\monitor_gpus" (
    echo Creating virtual environment 'monitor_gpus'...
    python -m venv "%PROJECT_ROOT%\monitor_gpus"
    if %ERRORLEVEL% NEQ 0 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

:: Activate virtual environment and install requirements
call "%PROJECT_ROOT%\monitor_gpus\Scripts\activate"
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

:: Check if requirements need to be installed
if not exist "%PROJECT_ROOT%\monitor_gpus\Lib\site-packages\psutil" (
    echo Installing requirements...
    pip install -r "%PROJECT_ROOT%\requirements.txt"
    if %ERRORLEVEL% NEQ 0 (
        echo Error: Failed to install requirements
        pause
        exit /b 1
    )
)

:: Run the monitor with 1 second refresh rate
python "%PROJECT_ROOT%\src\monitor_gpus.py" --interval 1.0 --refresh-rate 1.0

:: If the script exits, wait for user input
pause

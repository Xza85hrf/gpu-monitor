@echo off
echo Running GPU Monitor Tests...

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

:: Install requirements if needed
if not exist "%PROJECT_ROOT%\monitor_gpus\Lib\site-packages\psutil" (
    echo Installing requirements...
    pip install -r "%PROJECT_ROOT%\requirements.txt"
    pip install pytest pytest-cov
 coverage
    if %ERRORLEVEL% NEQ 0 (
        echo Error: Failed to install requirements
        pause
        exit /b 1
    )
)

:: Run the tests with coverage report
python -m pytest "%PROJECT_ROOT%\scripts\test_monitor_gpus.py" -v

:: If the script exits, wait for user input
pause
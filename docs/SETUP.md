# Detailed Setup Guide

## System Requirements

### Hardware Requirements

- NVIDIA GPU(s)
- Minimum 4GB RAM
- 100MB free disk space

### Software Requirements

- Windows 10/11
- Python 3.6 or higher
- NVIDIA GPU drivers
- Git (optional, for cloning repository)

## Installation Steps

### 1. Python Installation

1. Download Python from [python.org](https://python.org)
2. During installation:
   - ✅ Check "Add Python to PATH"
   - ✅ Check "Install pip"
3. Verify installation:

   ```cmd
   python --version
   pip --version
   ```

### 2. NVIDIA Drivers

1. Visit [NVIDIA Driver Downloads](https://www.nvidia.com/Download/index.aspx)
2. Select your GPU model
3. Download and install the latest driver
4. Verify installation in Device Manager

### 3. Project Setup

#### Option 1: Automated Setup (Recommended)

1. Navigate to the project directory
2. Run `scripts/run_gpu_monitor.bat`
3. The script automatically handles:
   - Virtual environment creation
   - Dependencies installation
   - Initial configuration

#### Option 2: Manual Setup

1. Create virtual environment:

   ```cmd
   python -m venv monitor_gpus
   ```

2. Activate virtual environment:

   ```cmd
   monitor_gpus\Scripts\activate

   ```

3. Install dependencies:

   ```cmd
   pip install -r requirements.txt
   ```

4. For development, install additional packages:

   ```cmd
   pip install pytest pytest-cov
   ```

## Directory Structure Setup

The project requires the following directory structure:

```directory
GPU_monitor/
├── src/              # Source code
├── scripts/          # Utility scripts
├── logs/            # Log files (created automatically)
├── monitor_gpus/    # Virtual environment
└── docs/            # Documentation
```

The `logs` directory will be created automatically when the application runs.

## Environment Variables

No special environment variables are required for basic operation.

## Troubleshooting

### Common Issues

1. "Python is not recognized":
   - Solution: Add Python to PATH environment variable
   - Reinstall Python with "Add to PATH" option checked

2. "NVIDIA drivers not found":
   - Verify driver installation in Device Manager
   - Update or reinstall NVIDIA drivers
   - Check GPU compatibility

3. "Import Error: No module named 'pynvml'":
   - Activate virtual environment
   - Reinstall requirements:

     ```cmd
     pip install -r requirements.txt
     ```

4. "Permission denied" for log files:
   - Ensure write permissions for logs directory
   - Run terminal as administrator if needed

### Verification Steps

1. Check Python installation:

   ```cmd
   python --version
   ```

2. Verify virtual environment:

   ```cmd
   monitor_gpus\Scripts\activate
   python -c "import pynvml; pynvml.nvmlInit()"

   ```

3. Test GPU access:

   ```cmd
   python scripts/test_monitor_gpus.py -v
   ```

## Updates and Maintenance

1. Update dependencies:

   ```cmd
   pip install --upgrade -r requirements.txt
   ```

2. Clear logs:

   ```cmd
   del /Q logs\*
   ```

3. Rebuild virtual environment:

   ```cmd
   deactivate
   rmdir /S /Q monitor_gpus
   scripts/run_gpu_monitor.bat
   ```

For additional help, see [README.md](README.md) or create an issue on GitHub.

# Quick Start Guide

## Installation

### Automatic Setup (Recommended)

1. Double-click `scripts/run_gpu_monitor.bat`

That's it! The script will:

- Create a virtual environment
- Install dependencies
- Start the monitor

### Manual Setup

1. Open a terminal in the project root
2. Create virtual environment:

   ```cmd
   python -m venv monitor_gpus
   monitor_gpus\Scripts\activate

   ```

3. Install dependencies:

   ```cmd
   pip install -r requirements.txt
   ```

3. Run monitor:

   ```cmd
   python src/monitor_gpus.py
   ```

## Basic Commands

### Start Monitor

```cmd
python src/monitor_gpus.py
```

### Monitor Specific GPUs

```cmd
python src/monitor_gpus.py --gpu-indices 0 1
```

### Custom Update Interval

```cmd
python src/monitor_gpus.py --interval 1.0
```

### Run Tests

```cmd
scripts/run_tests.bat
```

## Key Features

### Color Indicators

- 🔵 Blue: Low/Cool
- 🟢 Green: Normal
- 🟡 Yellow: Warning
- 🔴 Red: Critical

### Keyboard Controls

- `Ctrl+C`: Exit monitor

### Log Files

- Application logs: `logs/gpu_monitor.log`
- Test logs: `logs/test_gpu_monitor.log`

For more detailed information, see [README.md](README.md).

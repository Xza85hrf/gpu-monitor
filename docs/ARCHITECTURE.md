# GPU Monitor Project Architecture

## Directory Structure

```directory
GPU_monitor/
├── docs/                # Documentation files
├── logs/               # Log files directory
├── scripts/            # Utility and test scripts
│   ├── run_gpu_monitor.bat
│   ├── run_tests.bat
│   ├── test_monitor_gpus.py
│   └── toggle_gpu.bat
└── monitor_gpus.py     # Main application source
```

## Current Architecture

### Core Components

1. **Main Application (monitor_gpus.py)**
   - Real-time GPU monitoring using pynvml
   - System memory monitoring using psutil
   - Rich terminal interface for visualization
   - Configurable refresh rates and GPU selection
   - Comprehensive logging system

2. **Test Suite (test_monitor_gpus.py)**
   - Unit tests for all core functionality
   - Mock-based testing for GPU interactions
   - Coverage reporting
   - Integration with CI/CD pipelines

3. **Utility Scripts**
   - Automated environment setup (run_gpu_monitor.bat)
   - Test execution (run_tests.bat)
   - GPU control (toggle_gpu.bat)

### Design Patterns

1. **Modular Design**
   - Separation of concerns between monitoring, visualization, and logging
   - Reusable utility functions for common operations
   - Configurable thresholds and parameters

2. **Error Handling**
   - Comprehensive error handling for GPU operations
   - Graceful degradation when features are unavailable
   - Detailed logging of errors and warnings

3. **Configuration Management**
   - Command-line argument parsing
   - Environment-based configuration
   - Default values with override capability

### Logging System

- Centralized logging configuration
- Rotating log files in logs/ directory
- Timestamped entries with process IDs
- Multiple log levels (INFO, WARNING, ERROR)

### Testing Strategy

- Unit tests for all core functionality
- Integration tests for end-to-end monitoring
- Coverage reporting with pytest-cov
- Automated test execution via batch scripts

## Benefits

- Real-time monitoring with minimal overhead
- Cross-platform compatibility (Windows-focused)
- Comprehensive logging for debugging
- Automated setup and testing
- Maintainable and extensible architecture

## Future Improvements

1. Add support for Linux systems
2. Implement web-based monitoring interface
3. Add historical data tracking
4. Implement alerting system
5. Add support for AMD GPUs

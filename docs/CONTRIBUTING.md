# Contributing to GPU Monitor

Thank you for your interest in contributing to GPU Monitor! This document provides guidelines and best practices for contributing to the project.

## Development Setup

1. Fork the repository
2. Clone your fork:

   ```cmd
   git clone https://github.com/Xza85hrf/gpu-monitor.git
   cd gpu-monitor
   ```

3. Set up development environment:

   ```cmd
   python -m venv monitor_gpus
   monitor_gpus\Scripts\activate
   pip install -r requirements.txt
   pip install pytest pytest-cov ruff black

   ```

## Code Style Guidelines

### Python Code Style

- Follow PEP 8 conventions
- Use Black for code formatting
- Use Ruff for linting
- Maximum line length: 88 characters (Black default)
- Use descriptive variable names
- Include docstrings for all functions and classes

Example:

```python
def get_gpu_info(handle):
    """Get information for a single GPU.
    
    Args:
        handle: NVML device handle
        
    Returns:
        dict: GPU information including memory, utilization, temperature
        
    Raises:
        NVMLError: If GPU information cannot be retrieved
    """
    try:
        info = {}
        # Implementation
        return info
    except NVMLError as e:
        logging.error(f"Error getting GPU info: {str(e)}")
        return None
```

### Commits and Pull Requests

1. Create a feature branch:

   ```cmd
   git checkout -b feature/your-feature-name
   ```

2. Commit messages should:
   - Have a clear subject line
   - Explain what and why in the body
   - Reference issues if applicable

   Example:

   ```list
   Add GPU power limit monitoring

   - Implement power limit detection
   - Add color coding for power usage
   - Update documentation with power metrics

   Fixes #123
   ```

3. Keep commits focused and atomic

## Testing Requirements

### Writing Tests

1. Add tests for all new functionality
2. Maintain or improve code coverage
3. Use meaningful test names and descriptions
4. Include both positive and negative test cases

Example:

```python
def test_temperature_colors(self):
    """Test temperature color thresholds"""
    test_cases = [
        (35, "bright_blue"),  # Cold
        (45, "green"),        # Normal
        (65, "yellow"),       # Warm
        (85, "red")          # Hot
    ]
    for temp, expected_color in test_cases:
        with self.subTest(temp=temp):
            self.assertEqual(get_temp_color(temp), expected_color)
```

### Running Tests

1. Run the full test suite:

   ```cmd
   scripts/run_tests.bat
   ```

2. Check code coverage:
   - Minimum coverage requirement: 80%
   - Coverage report is generated automatically

### Logging

1. Use appropriate log levels:
   - ERROR: For errors that need attention
   - INFO: For significant events
   - DEBUG: For detailed debugging

2. Include relevant context in log messages
3. Use f-strings for log formatting

Example:

```python
logging.error(f"Failed to initialize GPU {gpu_id}: {str(error)}")
logging.info(f"Monitoring started for {len(gpus)} GPUs")
logging.debug(f"GPU {gpu_id} temperature: {temp}°C")
```

## Directory Structure

```directory
GPU_monitor/
├── src/              # Source code
├── scripts/          # Utility scripts
 (Windows batch files)
├── logs/            # Log files
├── docs/            # Documentation
└── tests/           # Test files
```

## Documentation

1. Update relevant documentation for new features
2. Include docstrings for all public functions/classes
3. Update CHANGELOG.md for all changes
4. Keep README.md current with new features

## Review Process

1. Create a pull request with:
   - Clear description of changes
   - Screenshots if applicable
   - Test results
   - Documentation updates

2. Address review comments promptly

3. Ensure all checks pass:
   - Tests passing
   - Code coverage maintained
   - Linting clean
   - Documentation updated

## Release Process

1. Update version numbers
2. Update CHANGELOG.md
3. Create release notes
4. Tag release in git

## Questions?

Feel free to:

- Open an issue for questions
- Join discussions in existing issues
- Contact maintainers directly

Thank you for contributing to GPU Monitor!

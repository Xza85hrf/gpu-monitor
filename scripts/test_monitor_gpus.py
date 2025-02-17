import os
import sys
import unittest
import logging
from unittest.mock import patch, MagicMock
import pynvml

from src.monitor_gpus import (
    get_temp_color,
    get_util_color,
    format_memory,
    create_status_bar,
    format_pcie,
    get_gpu_info,
    get_system_ram
)

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Configure test logging
LOGS_DIR = os.path.join(project_root, '../logs')
os.makedirs(LOGS_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOGS_DIR, 'test_gpu_monitor.log'),
    level=logging.INFO,
    format='%(asctime)s - [PID:%(process)d] - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class TestGPUMonitor(unittest.TestCase):
    def setUp(self):
        logging.info("Setting up test case")
        self.mock_handle = MagicMock()
        
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

    def test_utilization_colors(self):
        """Test utilization color thresholds"""
        test_cases = [
            (25, "bright_blue"),  # Low
            (45, "green"),        # Normal
            (75, "yellow"),       # High
            (95, "red")          # Critical
        ]
        for util, expected_color in test_cases:
            with self.subTest(util=util):
                self.assertEqual(get_util_color(util), expected_color)

    def test_format_memory(self):
        """Test memory formatting"""
        test_cases = [
            (1024**3, "1.0"),        # 1 GB
            (1024**3 * 1.5, "1.5"),  # 1.5 GB
            (1024**3 * 0.5, "0.5")   # 0.5 GB
        ]
        for bytes_value, expected in test_cases:
            with self.subTest(bytes=bytes_value):
                self.assertEqual(format_memory(bytes_value), expected)

    def test_create_status_bar(self):
        """Test status bar creation"""
        test_cases = [
            (0, 5, "[bright_blue]░░░░░[/]   0.0%"),
            (50, 5, "[green]██░░░[/]  50.0%"),
            (100, 5, "[red]█████[/] 100.0%")
        ]
        for percentage, width, expected in test_cases:
            with self.subTest(percentage=percentage):
                result = create_status_bar(percentage, width)
                self.assertIn(str(float(percentage)), result)
                self.assertTrue(any(color in result for color in ["bright_blue", "green", "yellow", "red"]))

    def test_format_pcie(self):
        """Test PCIe formatting"""
        self.assertEqual(format_pcie(4, 16), "Gen 4 x16")
        self.assertEqual(format_pcie(3, 8), "Gen 3 x8")

    @patch('pynvml.nvmlDeviceGetName')
    @patch('pynvml.nvmlDeviceGetMemoryInfo')
    @patch('pynvml.nvmlDeviceGetUtilizationRates')
    @patch('pynvml.nvmlDeviceGetTemperature')
    @patch('pynvml.nvmlDeviceGetPowerUsage')
    @patch('pynvml.nvmlDeviceGetMaxPcieLinkGeneration')
    @patch('pynvml.nvmlDeviceGetMaxPcieLinkWidth')
    def test_get_gpu_info(self, mock_pcie_width, mock_pcie_gen, mock_power, 
                         mock_temp, mock_util, mock_memory, mock_name):
        """Test GPU information gathering"""
        # Setup mock returns
        mock_name.return_value = "NVIDIA GeForce RTX 3090"
        mock_memory.return_value = MagicMock(used=5*1024**3, total=24*1024**3)
        mock_util.return_value = MagicMock(gpu=50)
        mock_temp.return_value = 65
        mock_power.return_value = 250000  # 250W in milliwatts
        mock_pcie_gen.return_value = 4
        mock_pcie_width.return_value = 16

        info = get_gpu_info(self.mock_handle)
        
        self.assertIsNotNone(info)
        self.assertEqual(info['name'], "GeForce RTX 3090")
        self.assertEqual(float(info['mem_used']), 5.0)
        self.assertEqual(float(info['mem_total']), 24.0)
        self.assertEqual(info['gpu_util'], 50)
        self.assertEqual(info['temp'], 65)
        self.assertEqual(info['power'], 250.0)
        self.assertEqual(info['pcie_gen'], 4)
        self.assertEqual(info['pcie_width'], 16)

    @patch('src.monitor_gpus.psutil.virtual_memory')
    def test_system_ram(self, mock_memory):
        """Test system RAM information gathering"""
        # Setup mock returns
        mock_memory.return_value = MagicMock(
            total=32*1024**3,
            used=16*1024**3,
            percent=50.0
        )

        ram_info = get_system_ram()
        
        self.assertIsNotNone(ram_info)
        self.assertEqual(float(ram_info['total']), 32.0)
        self.assertEqual(float(ram_info['used']), 16.0)
        self.assertEqual(ram_info['percent'], 50.0)

    def test_error_handling(self):
        """Test error handling for GPU info gathering"""
        with patch('pynvml.nvmlDeviceGetName') as mock_name:
            # Create a proper NVML error with an integer error code
            mock_name.side_effect = pynvml.NVMLError(1)  # Using error code 1
            info = get_gpu_info(self.mock_handle)
            self.assertIsNone(info)

if __name__ == '__main__':
    logging.info("Starting GPU Monitor tests")
    unittest.main(verbosity=2)
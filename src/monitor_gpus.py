import time
import psutil
from pathlib import Path
import pynvml
import logging
import argparse
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich import box
from rich.panel import Panel
from rich.align import Align

console = Console()

PROJECT_ROOT = Path(__file__).parent

# Ensure logs directory exists
LOGS_DIR = PROJECT_ROOT / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

# Set up logging with absolute path
LOG_FILE = LOGS_DIR / 'gpu_monitor.log'

# Configure logging
logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    # Add timestamps and process ID for better debugging
    format='%(asctime)s - [PID:%(process)d] - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Instructions panel text
INSTRUCTIONS = """
[cyan]Keyboard Controls:[/]
[green]Ctrl+C[/]: Exit monitor

[cyan]Color Indicators:[/]
[bright_blue]Blue[/]: Low/Cool     [green]Green[/]: Normal
[yellow]Yellow[/]: Warning   [red]Red[/]: Critical

[cyan]Metrics Ranges:[/]
Temperature: <40°C → >80°C
Utilization: <30% → >90%
Memory: <30% → >90%"""

# Thresholds for different metrics
TEMPERATURE_THRESHOLDS = {
    'cold': 40,
    'warm': 60,
    'hot': 80
}

UTILIZATION_THRESHOLDS = {
    'low': 30,
    'medium': 70,
    'high': 90
}

MEMORY_THRESHOLDS = {
    'low': 30,
    'medium': 70,
    'high': 90
}

def get_temp_color(temp):
    """Get color for temperature value"""
    if temp >= TEMPERATURE_THRESHOLDS['hot']:
        return "red"
    elif temp >= TEMPERATURE_THRESHOLDS['warm']:
        return "yellow"
    elif temp >= TEMPERATURE_THRESHOLDS['cold']:
        return "green"
    return "bright_blue"

def get_util_color(util):
    """Get color for utilization value"""
    if util >= UTILIZATION_THRESHOLDS['high']:
        return "red"
    elif util >= UTILIZATION_THRESHOLDS['medium']:
        return "yellow"
    elif util >= UTILIZATION_THRESHOLDS['low']:
        return "green"
    return "bright_blue"

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='GPU and System Memory Monitor')
    parser.add_argument('--interval', type=float, default=2.0,
                       help='Update interval in seconds (default: 2.0)')
    parser.add_argument('--gpu-indices', type=int, nargs='+',
                       help='Specific GPU indices to monitor (default: all GPUs)')
    parser.add_argument('--refresh-rate', type=float, default=1.0,
                       help='Screen refresh rate in seconds (default: 1.0)')
    return parser.parse_args()

def format_memory(value):
    """Format memory values in GB"""
    return f"{value/1024**3:.1f}"

def create_status_bar(percentage, width=15):
    """Create a colored progress bar based on percentage"""
    percentage = round(percentage, 1)
    filled = int(percentage * width / 100)
    color = get_util_color(percentage)
    bar = f"[{color}]{'█' * filled}{'░' * (width-filled)}[/]"
    return f"{bar} {percentage:>4.1f}%"

def format_pcie(gen, width):
    """Format PCIe information"""
    return f"Gen {gen} x{width}"

def get_gpu_info(handle):
    """Get information for a single GPU"""
    try:
        info = {}
        info['name'] = pynvml.nvmlDeviceGetName(handle).replace("NVIDIA ", "")
        
        # Memory info
        mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
        info['mem_used'] = format_memory(mem.used)
        info['mem_total'] = format_memory(mem.total)
        info['mem_percent'] = (mem.used / mem.total) * 100
        
        # Utilization info
        util = pynvml.nvmlDeviceGetUtilizationRates(handle)
        info['gpu_util'] = util.gpu
        
        # Temperature
        info['temp'] = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
        
        # Power usage
        power_watts = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0
        info['power'] = power_watts
        
        # PCIe info
        info['pcie_gen'] = pynvml.nvmlDeviceGetMaxPcieLinkGeneration(handle)
        info['pcie_width'] = pynvml.nvmlDeviceGetMaxPcieLinkWidth(handle)
        
        return info
    
    except pynvml.NVMLError as e:
        logging.error(f"Error getting GPU info: {str(e)}")
        return None

def get_system_ram():
    """Get system RAM information"""
    try:
        ram = psutil.virtual_memory()
        return {
            'used': format_memory(ram.used),
            'total': format_memory(ram.total),
            'percent': ram.percent
        }
    except Exception as e:
        logging.error(f"Error getting system RAM info: {str(e)}")
        return None

def create_monitor_table():
    """Create and configure the monitoring table"""
    table = Table(
        box=box.SIMPLE,
        title="GPU and System Memory Monitor",
        title_style="bold magenta",
        show_header=True,
        header_style="bold cyan",
        show_edge=False,
        padding=(0, 1),
        collapse_padding=True
    )
    
    table.add_column("Device", no_wrap=True)
    table.add_column("Utilization", justify="left")
    table.add_column("Memory", justify="left")
    table.add_column("Temp", justify="right")
    table.add_column("Power", justify="right")
    table.add_column("PCIe", justify="center")
    
    return table

def create_display():
    """Create the complete display with instructions and monitoring table"""
    # Create the instructions panel
    instructions = Panel(
        Align.right(INSTRUCTIONS),
        title="Quick Guide",
        border_style="bright_blue",
        padding=(1, 2),
        width=40
    )
    
    # Return both components
    return instructions

def main():
    args = parse_arguments()
    
    try:
        pynvml.nvmlInit()
        device_count = pynvml.nvmlDeviceGetCount()
        logging.info(f"Initialized NVML. Found {device_count} GPU(s)")
        
        gpu_indices = args.gpu_indices if args.gpu_indices else range(device_count)
        gpu_indices = [i for i in gpu_indices if 0 <= i < device_count]
        
        if not gpu_indices:
            logging.error("No valid GPU indices specified")
            console.print("[bold red]Error: No valid GPU indices specified[/bold red]")
            return
        
        # Print instructions panel
        console.print(create_display())
        console.print()  # Add some spacing
        
        with Live(refresh_per_second=args.refresh_rate) as live:
            while True:
                table = create_monitor_table()
                
                # Add GPU information
                for i in gpu_indices:
                    try:
                        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                        gpu_info = get_gpu_info(handle)
                        
                        if gpu_info:
                            # Color-coded utilization bar
                            util_bar = create_status_bar(gpu_info['gpu_util'])
                            
                            # Color-coded memory bar
                            mem_bar = create_status_bar(gpu_info['mem_percent'])
                            
                            # Color-coded temperature
                            temp_color = get_temp_color(gpu_info['temp'])
                            temp_display = f"[{temp_color}]{gpu_info['temp']}°C[/]"
                            
                            # Color-coded power based on typical TDP
                            power_str = f"{gpu_info['power']:.1f}W"
                            
                            table.add_row(
                                gpu_info['name'],
                                util_bar,
                                f"{mem_bar}\n{gpu_info['mem_used']}/{gpu_info['mem_total']} GB",
                                temp_display,
                                power_str,
                                format_pcie(gpu_info['pcie_gen'], gpu_info['pcie_width'])
                            )
                        else:
                            table.add_row(
                                f"GPU {i} [red](Error)[/]",
                                "[red]Error[/]",
                                "[red]Error[/]",
                                "-",
                                "-",
                                "-"
                            )
                    except pynvml.NVMLError as e:
                        logging.error(f"Error monitoring GPU {i}: {str(e)}")
                
                # Add System RAM information
                ram_info = get_system_ram()
                if ram_info:
                    ram_bar = create_status_bar(ram_info['percent'])
                    table.add_row(
                        "[yellow]System RAM[/]",
                        ram_bar,
                        f"{ram_bar}\n{ram_info['used']}/{ram_info['total']} GB",
                        "-",
                        "-",
                        "-"
                    )
                
                live.update(table)
                time.sleep(args.interval)
    
    except KeyboardInterrupt:
        console.print("\n[bold red]Monitoring stopped.[/bold red]")
        logging.info("Monitoring stopped by user")
    except Exception as e:
        console.print(f"\n[bold red]Error: {str(e)}[/bold red]")
        logging.error(f"Unexpected error: {str(e)}")
    finally:
        pynvml.nvmlShutdown()
        logging.info("NVML shutdown complete")

if __name__ == "__main__":
    main()

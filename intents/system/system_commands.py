import os
import socket
import psutil
import subprocess
import re
from typing import Dict, List, Any, Union
from datetime import datetime

import requests

class SystemCommands:
    def __init__(self):
        # Basic settings
        self.thingsboard_url = "http://demo.thingsboard.io/api/v1/"  # Update with your ThingsBoard URL
        self.device_token = "0cwapzhu90f0qiyc59bh"  # Replace with your actual device access token
        self.maintenance_enabled = True
        self.shutdown_delay = 5  # seconds
        
        # Map functions to their trigger patterns
        self.command_map = {
            self.check_cpu_status: [
                r'cpu (status|usage|info)',
                r'processor (status|usage)',
                r'check cpu'
            ],
            self.check_system_status: [
                r'system (status|health)',
                r'check system',
                r'system overview',
                r'system diagnostics'
            ],
            self.check_disk_space: [
                r'disk (space|usage|status)',
                r'storage (space|usage)',
                r'drive space'
            ],
            self.check_network: [
                r'network (status|connection)',
                r'check (network|internet)',
                r'connectivity'
            ],
            self.get_ip_address: [
                r'(ip|network) address',
                r'my ip',
                r'show ip'
            ],
            self.hibernate_system: [
                r'hibernate (system|computer|pc)',
                r'sleep (system|computer|pc)',
                r'put to sleep'
            ],
            self.restart_system: [
                r'restart (system|computer|pc)',
                r'reboot (system|computer|pc)',
                r'system restart'
            ],
            self.shutdown_system: [
                r'shutdown (system|computer|pc)',
                r'power off',
                r'turn off (system|computer|pc)'
            ],
            self.system_maintenance: [
                r'maintenance',
                r'system maintenance',
                r'clean(up)? system',
                r'optimize system'
            ],
              self.turn_on_bulb: [
                r'turn on (smart )?bulb',
                r'light on',
                r'switch on bulb'
            ],
            self.turn_off_bulb: [
                r'turn off (smart )?bulb',
                r'light off',
                r'switch off bulb'
            ]
        }

    def check_cpu_status(self) -> Dict[str, Union[float, str]]:
        """Get detailed CPU and battery status."""
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            cpu_freq = psutil.cpu_freq()
            battery = psutil.sensors_battery()
            
            status = {
                'cpu_usage': cpu_usage,
                'cpu_frequency': f"{round(cpu_freq.current, 2)} MHz",
                'cpu_cores': psutil.cpu_count(),
                'timestamp': datetime.now().isoformat()
            }
            
            if battery:
                status.update({
                    'battery_level': battery.percent,
                    'battery_plugged': battery.power_plugged,
                    'battery_time_left': str(battery.secsleft) if battery.secsleft != -1 else 'Unknown'
                })
                
            return status
        except Exception as e:
            return {'error': f"Failed to get CPU status: {str(e)}"}

    def check_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status information."""
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'cpu': self.check_cpu_status(),
                'memory': {
                    'total': f"{round(memory.total / (1024**3), 2)} GB",
                    'used': f"{round(memory.used / (1024**3), 2)} GB",
                    'percent': memory.percent
                },
                'swap': {
                    'total': f"{round(swap.total / (1024**3), 2)} GB",
                    'used': f"{round(swap.used / (1024**3), 2)} GB",
                    'percent': swap.percent
                },
                'disk': self.check_disk_space(),
                'network': self.check_network(),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {'error': f"Failed to get system status: {str(e)}"}

    def check_disk_space(self) -> Dict[str, float]:
        """Get detailed disk space information."""
        try:
            disk = psutil.disk_usage('/')
            io_counters = psutil.disk_io_counters()
            
            return {
                'total_gb': round(disk.total / (2**30), 2),
                'used_gb': round(disk.used / (2**30), 2),
                'free_gb': round(disk.free / (2**30), 2),
                'percent_used': disk.percent,
                'read_mb': round(io_counters.read_bytes / (2**20), 2),
                'write_mb': round(io_counters.write_bytes / (2**20), 2)
            }
        except Exception as e:
            return {'error': f"Failed to get disk space info: {str(e)}"}

    def check_network(self) -> Dict[str, Any]:
        """Get comprehensive network status."""
        try:
            # Test internet connectivity
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            network_info = psutil.net_if_stats()
            net_io = psutil.net_io_counters()
            
            return {
                'status': 'Connected',
                'interfaces': {
                    interface: {
                        'up': stats.isup,
                        'speed': stats.speed,
                        'mtu': stats.mtu
                    }
                    for interface, stats in network_info.items()
                },
                'io_stats': {
                    'bytes_sent': round(net_io.bytes_sent / (2**20), 2),
                    'bytes_recv': round(net_io.bytes_recv / (2**20), 2),
                    'packets_sent': net_io.packets_sent,
                    'packets_recv': net_io.packets_recv
                }
            }
        except Exception as e:
            return {'status': 'Disconnected', 'error': str(e)}

    def get_ip_address(self) -> Dict[str, str]:
        """Get both local and public IP addresses."""
        try:
            # Get local IP
            local_ip = socket.gethostbyname(socket.gethostname())
            
            # Get public IP (requires internet connection)
            public_ip = subprocess.check_output(
                ['curl', 'ifconfig.me'],
                universal_newlines=True
            ).strip()
            
            return {
                'local_ip': local_ip,
                'public_ip': public_ip,
                'hostname': socket.gethostname()
            }
        except Exception as e:
            return {'error': f"Failed to get IP addresses: {str(e)}"}

    def hibernate_system(self) -> str:
        """Hibernate the system safely."""
        try:
            if os.name == 'nt':  # Windows
                os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
                return "System hibernation initiated"
        except Exception as e:
            return f"Failed to hibernate system: {str(e)}"

    def restart_system(self) -> str:
        """Restart the system safely."""
        try:
            if os.name == 'nt':  # Windows
                os.system(f"shutdown /r /t {self.shutdown_delay}")
            else:  # Linux/Unix
                os.system(f"shutdown -r {self.shutdown_delay}")
            return f"System restart scheduled in {self.shutdown_delay} seconds"
        except Exception as e:
            return f"Failed to restart system: {str(e)}"

    def shutdown_system(self) -> str:
        """Shutdown the system safely."""
        try:
            if os.name == 'nt':  # Windows
                os.system(f"shutdown /s /t {self.shutdown_delay}")
            return f"System shutdown scheduled in {self.shutdown_delay} seconds"
        except Exception as e:
            return f"Failed to shutdown system: {str(e)}"

    def system_maintenance(self) -> Dict[str, Any]:
        """Perform system maintenance tasks."""
        if not self.maintenance_enabled:
            return {'status': 'Maintenance disabled'}
            
        results = {}
        try:
            # Clear temporary files
            if os.name == 'nt':  # Windows
                os.system('del /f /s /q %temp%\*')
                results['temp_cleanup'] = "Completed"
                
                # Run disk cleanup
                os.system('cleanmgr /sagerun:1')
                results['disk_cleanup'] = "Initiated"
                
                # Check disk health
                os.system('chkdsk /f')
                results['disk_check'] = "Scheduled"
            
            results['status'] = "Maintenance tasks completed"
            return results
        except Exception as e:
            return {'error': f"Maintenance failed: {str(e)}"}

    def turn_on_bulb(self,command) -> str:
        """Turn on the smart bulb."""
        try:
            payload = {"bulbStatus": "on"}
            response = requests.post(
                f"{self.thingsboard_url}{self.device_token}/telemetry",
                headers={"Content-Type": "application/json"},
                json=payload
            )
            if response.status_code == 200:
                return "Smart bulb turned on."
            else:
                return f"Failed to turn on bulb: {response.text}"
        except Exception as e:
            return f"Error: {str(e)}"

    def turn_off_bulb(self,command) -> str:
        """Turn off the smart bulb."""
        try:
            payload = {"bulbStatus": "off"}
            response = requests.post(
                f"{self.thingsboard_url}{self.device_token}/telemetry",
                headers={"Content-Type": "application/json"},
                json=payload
            )
            if response.status_code == 200:
                return "Smart bulb turned off."
            else:
                return f"Failed to turn off bulb: {response.text}"
        except Exception as e:
            return f"Error: {str(e)}"
        
    def execute_command(self, command: str) -> Any:
        """Execute the command based on the given input pattern."""
        command = command.lower()
        
        for func, patterns in self.command_map.items():
            for pattern in patterns:
                if re.search(pattern, command):
                    return func()
        
        return "Command not recognized"
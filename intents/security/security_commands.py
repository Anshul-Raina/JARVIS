import os
import subprocess
import datetime
import re
from typing import Dict, List, Callable, Any

class SecurityCommands:
    def __init__(self):
        # Basic assistant settings
        self.speech_rate = 150
        self.volume = 1.0
        self.quiet_mode = False

        # Map functions to their trigger patterns
        self.command_map = {
            self.lock_computer: [
                r'lock (computer|pc|system)',
                r'secure (computer|pc|system)',
                r'lock workstation'
            ],
            self.security_check: [
                r'security check',
                r'check security',
                r'system security',
                r'security status',
                r'check firewall'
            ],
            self.get_security_info: [
                r'security info',
                r'system info',
                r'security information',
                r'system details'
            ]
        }

    def lock_computer(self) -> str:
        """Lock the computer workstation."""
        try:
            if os.name == 'nt':
                os.system('rundll32.exe user32.dll,LockWorkStation')
                return "Computer locked successfully"
            return "Lock command only supported on Windows"
        except Exception as e:
            return f"Error locking computer: {str(e)}"

    def security_check(self) -> Dict[str, Any]:
        """Perform a security check of the system."""
        try:
            firewall = subprocess.run(
                ['netsh', 'advfirewall', 'show', 'currentprofile'],
                capture_output=True,
                text=True
            )
            
            system_info = subprocess.run(
                ['systeminfo'],
                capture_output=True,
                text=True
            )

            return {
                'firewall': (
                    firewall.stdout if firewall.returncode == 0 
                    else "Firewall check failed"
                ),
                'system_info': (
                    system_info.stdout if system_info.returncode == 0 
                    else "System info check failed"
                ),
                'timestamp': datetime.datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'error': f"Security check failed: {str(e)}",
                'timestamp': datetime.datetime.now().isoformat()
            }

    def get_security_info(self) -> str:
        """Get a formatted summary of security information."""
        security_data = self.security_check()
        
        if 'error' in security_data:
            return security_data['error']
            
        summary = [
            "Security Information Summary:",
            f"Check Time: {security_data['timestamp']}",
            "\nFirewall Status:",
            *security_data['firewall'].split('\n')[:3],  # First 3 lines of firewall info
            "\nSystem Information:",
            *security_data['system_info'].split('\n')[:3]  # First 3 lines of system info
        ]
        
        return '\n'.join(summary)

    def execute_command(self, command: str) -> str:
        """Execute the command based on the given input."""
        command = command.lower()
        
        for func, patterns in self.command_map.items():
            for pattern in patterns:
                if re.search(pattern, command):
                    return func()
        
        return "Command not recognized"

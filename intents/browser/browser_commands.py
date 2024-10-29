import os
import datetime
from typing import Dict, List, Callable, Any
import pyautogui
import re

class BrowserCommands:
    def __init__(self):
        # Browser configuration
        self.active_browser = 'chrome'
        self.last_command_time = datetime.datetime.now()
        
        # Browser executable paths
        self.browser_paths = {
            'chrome': 'c:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
            'brave': 'c:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'
        }

        # Map functions to their trigger patterns
        self.command_map = {
            self.open_browser: [
                r'open (google|chrome)',
                r'open brave',
                r'launch (chrome|brave)',
                r'start (chrome|brave)'
            ],

            self.close_browser: [
                r'close (chrome|brave)',
                r'exit (chrome|brave)',
                r'quit (chrome|brave)'
            ],

            self.window_operations: [
                r'open new window',
                r'open incognito( window)?',
                r'minimize( window)?',
                r'maximize( window)?',
                r'close window'
            ],

            self.tab_operations: [
                r'open( new)? tab',
                r'close tab',
                r'reopen tab',
                r'switch tab',
                r'refresh all( tabs)?'
            ],

            self.browser_features: [
                r'(open )?downloads',
                r'(open )?history',
                r'(add )?bookmark( page)?',
                r'show bookmarks'
            ]
        }

    def tab_operations(self, command: str) -> str:
        """Handle tab-related operations with exact and partial match checking."""
        operations = {
            'open new tab': ('ctrl', 't'),
            'close tab': ('ctrl', 'w'),
            'reopen tab': ('ctrl', 'shift', 't'),
            'switch tab': ('ctrl', 'tab'),
            'refresh all tabs': ('ctrl', 'shift', 'r')
        }
        
        normalized_command = command.strip().lower()
        print(f"Received command: '{normalized_command}'")
        
        if normalized_command in operations:
            keys = operations[normalized_command]
            pyautogui.hotkey(*keys)
            print(f"Executing exact match for: {normalized_command}")
            return f"Tab operation '{normalized_command}' completed"
        
        for operation, keys in operations.items():
            if operation in normalized_command:
                pyautogui.hotkey(*keys)
                print(f"Executing partial match for: {operation}")
                return f"Tab operation '{operation}' completed"
        
        print("No matching tab operation found.")
        return "Invalid tab operation"

    def open_browser(self, command: str) -> str:
        """Open specified browser or default to Chrome"""
        browser = 'brave' if 'brave' in command.lower() else 'chrome'
        try:
            os.startfile(self.browser_paths[browser])
            self.active_browser = browser
            return f"{browser.title()} browser opened successfully"
        except Exception as e:
            return f"Error opening {browser}: {str(e)}"

    def close_browser(self, command: str) -> str:
        """Close specified browser"""
        browser = 'brave' if 'brave' in command.lower() else 'chrome'
        try:
            os.system(f'taskkill /im {browser}.exe /f')
            return f"{browser.title()} browser closed successfully"
        except Exception as e:
            return f"Error closing {browser}: {str(e)}"

    def window_operations(self, command: str) -> str:
        """Handle window-related operations"""
        if 'new window' in command:
            pyautogui.hotkey('ctrl', 'n')
            return "New window opened"
        elif 'incognito' in command:
            pyautogui.hotkey('ctrl', 'shift', 'n')
            return "Incognito window opened"
        elif 'minimize' in command:
            pyautogui.hotkey('win', 'down')
            return "Window minimized"
        elif 'maximize' in command:
            pyautogui.hotkey('win', 'up')
            return "Window maximized"
        elif 'close window' in command:
            pyautogui.hotkey('alt', 'f4')
            return "Window closed"
        return "Invalid window operation"


    def browser_features(self, command: str) -> str:
        """Handle browser features like downloads, history, and bookmarks"""
        features = {
            'downloads': ('ctrl', 'j'),
            'history': ('ctrl', 'h'),
            'bookmark': ('ctrl', 'd'),
            'show bookmarks': ('ctrl', 'shift', 'b')
        }
        
        for feature, keys in features.items():
            if feature in command:
                pyautogui.hotkey(*keys)
                return f"Opened {feature}"
        return "Invalid browser feature"

    def execute_command(self, command: str) -> str:
        """Execute the given browser command"""
        command = command.lower()
        
        for func, patterns in self.command_map.items():
            for pattern in patterns:
                if re.search(pattern, command):
                    return func(command)
                
        return "Command not recognized"

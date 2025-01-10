import logging
import os
import pyautogui
import re

class MediaCommands:
    def __init__(self):
        # Map functions to trigger patterns
        self.command_map = {
            self.volume_up: [
                r'volume up',
                r'increase volume'
            ],
            self.volume_down: [
                r'volume down',
                r'decrease volume'
            ],
            self.volume_mute: [
                r'mute',
                r'silence'
            ],
            self.take_screenshot: [
                r'take screenshot(.*)',
                r'capture screen as (.*)'
            ],
            self.open_camera: [
                r'open camera',
                r'launch camera'
            ]
        }

    def volume_up(self) -> str:
        pyautogui.press('volumeup')
        return "Volume increased"

    def volume_down(self) -> str:
        pyautogui.press('volumedown')
        return "Volume decreased"

    def volume_mute(self) -> str:
        pyautogui.press('volumemute')
        return "Volume unmuted"

    def take_screenshot(self, name: str) -> str:
        try:
            # Get the correct path to Desktop using OS-independent way
            desktop_path = os.path.expanduser("~/Desktop")
            
            # Ensure name has no extension and add .png
            name = name.split('.')[0]  # Remove any existing extension
            screenshot_path = os.path.join(desktop_path, f"{name}.png")
            
            # Take the screenshot using pyautogui
            screenshot = pyautogui.screenshot()
            
            # Ensure it's in RGB mode before saving
            if screenshot.mode != 'RGB':
                screenshot = screenshot.convert('RGB')
            
            # Save with explicit format
            screenshot.save(screenshot_path, format='PNG')
            
            return f"Screenshot saved as {screenshot_path}"
            
        except Exception as e:
            logging.error(f"Screenshot error: {str(e)}")
            return f"Error taking screenshot: {str(e)}"

    def open_camera(self) -> str:
        pyautogui.hotkey('win')
        pyautogui.typewrite('camera')
        pyautogui.hotkey('enter')
        return "Camera opened"

    def execute_command(self, command: str) -> str:
        command = command.lower()
        
        for func, patterns in self.command_map.items():
            for pattern in patterns:
                if re.search(pattern, command):
                    if func == self.take_screenshot:
                        # Extract the name for the screenshot
                        name = self._extract_text(command, 'screenshot')
                        return func(name)
                    return func()
        
        return "Command not recognized"

    def _extract_text(self, command: str, keyword: str) -> str:
        """Extract text after a keyword from command"""
        return command.split(keyword, 1)[1].strip() if keyword in command else ""

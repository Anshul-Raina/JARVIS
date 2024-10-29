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

    def volume_up(self,command) -> str:
        pyautogui.press('volumeup')
        return "Volume increased"

    def volume_down(self,command) -> str:
        pyautogui.press('volumedown')
        return "Volume decreased"

    def volume_mute(self,command) -> str:
        pyautogui.press('volumemute')
        return "Volume unmuted"

    def take_screenshot(self, name: str) -> str:
        img = pyautogui.screenshot()
        img.save(f'C:/Desktop/{name}.png')
        return f"Screenshot saved as {name}.png"

    def open_camera(self,command) -> str:
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

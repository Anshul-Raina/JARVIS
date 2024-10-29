from datetime import datetime
from typing import Dict, List, Callable, Any

class AssistantCommands:
    def __init__(self):
        self.speech_rate = 150
        self.volume = 1.0
        self.quiet_mode = False
        
        # Map functions to their trigger patterns
        self.command_map = {
            self.introduce: [
                r'who (are|r) you',
                r'what(?:\'s| is) your name',
                r'introduce yourself',
                r'tell me about yourself'
            ],
            
            self.creator_info: [
                r'who (created|made) you',
                r'who(?:\'s| is) your creator',
                r'who(?:\'s| is) your maker'
            ],
            
            self.adjust_speech_rate: [
                r'speak faster',
                r'increase speed',
                r'talk faster',
                r'speak slower',
                r'decrease speed',
                r'talk slower'
            ],
            
            self.set_quiet_mode: [
                r'quiet mode',
                r'silent mode',
                r'enable quiet mode',
                r'disable quiet mode'
            ],
            
            self.shutdown_assistant: [
                r'shutdown',
                r'exit',
                r'quit',
                r'goodbye',
                r'bye'
            ]
        }
    
    def introduce(self) -> str:  # Added command parameter here
        return "I am Jarvis, your personal AI assistant. I can help you with various tasks."
    
    def creator_info(self) -> str:  # Added command parameter here
        return "I was created by Sir, Anshul Raina using Python in Visual Studio Code."
    
    def adjust_speech_rate(self, command: str) -> str:
        direction = "faster" if any(word in command for word in ['faster', 'increase']) else "slower"
        adjustment = 25 if direction == "faster" else -25
        self.speech_rate = max(50, min(300, self.speech_rate + adjustment))
        return f"Speech rate adjusted to {self.speech_rate}"
    
    def set_quiet_mode(self, command: str) -> str:
        enable = not any(word in command for word in ['disable', 'off'])
        self.quiet_mode = enable
        self.volume = 0.5 if enable else 1.0
        return f"Quiet mode {'enabled' if enable else 'disabled'}"
    
    def shutdown_assistant(self) -> None:  # Added command parameter here
        quit()
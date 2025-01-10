from datetime import datetime
import re
import sys
from typing import Dict, List, Callable, Any

class AssistantCommands:
    def __init__(self):
        self.speech_rate = 150
        self.volume = 1.0
        self.quiet_mode = False
        self.name = "Jarvis"
        
        # Map functions to their trigger patterns
        self.command_map = {
            self.introduce: [
                r'who (are|r) you',
                r'what(?:\'s| is) your name',
                r'introduce yourself',
                r'tell me about yourself',
                r'what can you do',
                r'help',
                r'list commands',
                r'show commands'
            ],
            
            self.creator_info: [
                r'who (created|made) you',
                r'who(?:\'s| is) your creator',
                r'who(?:\'s| is) your maker',
                r'who designed you',
                r'who programmed you'
            ],
            
            self.adjust_speech_rate: [
                r'speak (faster|slower)',
                r'(increase|decrease) speed',
                r'talk (faster|slower)',
                r'adjust speech rate',
                r'change speech speed',
                r'speed up',
                r'slow down'
            ],
            
            self.adjust_volume: [
                r'(increase|decrease) volume',
                r'volume (up|down)',
                r'speak (louder|softer)',
                r'adjust volume',
                r'change volume'
            ],
            
            self.set_quiet_mode: [
                r'quiet mode',
                r'silent mode',
                r'enable quiet mode',
                r'disable quiet mode',
                r'turn on quiet mode',
                r'turn off quiet mode'
            ],
            
            self.get_capabilities: [
                r'what can you do',
                r'list capabilities',
                r'show features',
                r'what are your functions',
                r'list your abilities'
            ],
            
            self.get_status: [
                r'status',
                r'system status',
                r'how are you',
                r'check status',
                r'diagnostics'
            ],
            
            self.change_name: [
                r'change your name to (.+)',
                r'call yourself (.+)',
                r'set name to (.+)',
                r'rename to (.+)'
            ],
            
            self.shutdown_assistant: [
                r'shutdown',
                r'exit',
                r'quit',
                r'goodbye',
                r'bye',
                r'stop assistant',
                r'terminate'
            ]
        }
    
    def introduce(self, command: str = "") -> str:
        return (f"I am {self.name}, your personal AI assistant. I can help you with various tasks including:\n"
                "- Web searches (Google, YouTube, Wikipedia)\n"
                "- Answer questions using Wolfram Alpha\n"
                "- Control system functions\n"
                "- Manage files and applications\n"
                "- Set reminders and alarms\n"
                "Say 'what can you do' for a complete list of commands.")
    
    def creator_info(self, command: str = "") -> str:
        return "I was created by Sir, Anshul Raina using Python in Visual Studio Code."
    
    def adjust_speech_rate(self, command: str) -> str:
        if any(word in command for word in ['faster', 'increase', 'speed up']):
            self.speech_rate = min(300, self.speech_rate + 25)
            direction = "increased"
        else:
            self.speech_rate = max(50, self.speech_rate - 25)
            direction = "decreased"
        return f"Speech rate {direction} to {self.speech_rate}"
    
    def adjust_volume(self, command: str) -> str:
        if any(word in command for word in ['up', 'increase', 'louder']):
            self.volume = min(1.0, self.volume + 0.1)
            direction = "increased"
        else:
            self.volume = max(0.1, self.volume - 0.1)
            direction = "decreased"
        return f"Volume {direction} to {int(self.volume * 100)}%"
    
    def set_quiet_mode(self, command: str) -> str:
        enable = not any(word in command for word in ['disable', 'off'])
        self.quiet_mode = enable
        self.volume = 0.5 if enable else 1.0
        return f"Quiet mode {'enabled' if enable else 'disabled'}"
    
    def get_capabilities(self, command: str = "") -> str:
        capabilities = [
            "1. Web Searches:",
            "   - Google search",
            "   - YouTube search",
            "   - Wikipedia lookups",
            "2. Information:",
            "   - Answer questions (Wolfram Alpha)",
            "   - Get current time and date",
            "   - Check weather",
            "3. System Control:",
            "   - Open applications",
            "   - File management",
            "   - Volume control",
            "4. Assistant Settings:",
            "   - Adjust speech rate",
            "   - Change volume",
            "   - Enable/disable quiet mode"
        ]
        return "\n".join(capabilities)
    
    def get_status(self, command: str = "") -> str:
        return (f"Status Report:\n"
                f"Name: {self.name}\n"
                f"Speech Rate: {self.speech_rate}\n"
                f"Volume: {int(self.volume * 100)}%\n"
                f"Quiet Mode: {'Enabled' if self.quiet_mode else 'Disabled'}")
    
    def change_name(self, command: str) -> str:
        match = re.search(r'(?:change your name to|call yourself|set name to|rename to)\s+(.+)', command, re.IGNORECASE)
        if match:
            new_name = match.group(1).strip()
            self.name = new_name
            return f"My name has been changed to {new_name}"
        return "Please specify a new name"
    
    def shutdown_assistant(self) -> str:
        print("Shutting down. Goodbye!")
        sys.exit()
    
    def execute_command(self, command: str) -> str:
        """Execute the command based on the given input."""
        command = command.lower()
        
        for func, patterns in self.command_map.items():
            for pattern in patterns:
                match = re.search(pattern, command, re.IGNORECASE)
                if match:
                    return func(command)
        
        return "Command not recognized"
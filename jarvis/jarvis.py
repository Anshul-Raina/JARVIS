import datetime
import re
import pyttsx3
import speech_recognition as sr
from typing import Dict, List, Callable, Optional, Any
from dataclasses import dataclass
import os
import sys
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

try:
    from intents.assistant.assistant_commands import AssistantCommands
    from intents.browser.browser_commands import BrowserCommands
    from intents.information.information_commands import InformationCommands
    from intents.media.media_commands import MediaCommands
    from intents.productivity.productivity_commands import ProductivityCommands
    from intents.security.security_commands import SecurityCommands
    from intents.system.system_commands import SystemCommands
except ImportError as e:
    print(f"Import Error: {e}")
    print(f"Current sys.path: {sys.path}")
    print(f"Project root: {project_root}")
    sys.exit(1)

@dataclass
class CommandResult:
    success: bool
    message: str
    data: Optional[Any] = None

class Jarvis:
    def __init__(self):
        # Initialize speech engine
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        
        # Initialize command systems
        self.assistant_commands = AssistantCommands()
        self.productivity_commands = ProductivityCommands()
        self.system_commands = SystemCommands()
        self.browser_commands = BrowserCommands()
        self.media_commands = MediaCommands()
        self.security_commands=SecurityCommands()
        self.information_commands=InformationCommands()
        
        # Initialize state
        self.active = True
        self.last_command = None
        self.command_history = []
        
        # Set default voice properties
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)
        
        # Combined command mapping from all systems
        self.command_map = self._build_command_map()

    def _build_command_map(self) -> Dict[str, List[str]]:
        """Combines command patterns from all command systems"""
        command_map = {}
        
        # Add patterns from each command system
        systems = [
            self.assistant_commands,
            self.productivity_commands,
            self.system_commands,
            self.browser_commands,
            self.media_commands,
            self.security_commands,
            self.information_commands
        ]
        
        for system in systems:
            for func, patterns in system.command_map.items():
                command_map[func] = patterns
                
        return command_map

    def speak(self, text: str) -> None:
        """Speak the given text using text-to-speech"""
        print(f"Jarvis: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self) -> str:
        """Listen for user input through microphone"""
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.pause_threshold = 1
            audio = self.recognizer.listen(source)
            
        try:
            print("Recognizing...")
            query = self.recognizer.recognize_google(audio, language='en-US')
            query = query.lower()
            print(f"User: {query}")
            return query
        except Exception as e:
            print(f"Error in speech recognition: {str(e)}")
            return "None"

    def execute_command(self, command: str) -> CommandResult:
        """Execute the given command by matching it to appropriate handler"""
        # Store command in history
        self.command_history.append((datetime.datetime.now(), command))
        self.last_command = command

        # Check each command pattern for a match
        for func, patterns in self.command_map.items():
            for pattern in patterns:
                match = re.search(pattern, command)
                if match:
                    try:
                        # Extract the relevant part of the command
                        result = func(command)  # Pass the full command to the function
                        return CommandResult(
                            success=True,
                            message="Command executed successfully",
                            data=result
                        )
                    except Exception as e:
                        return CommandResult(
                            success=False,
                            message=f"Error executing command: {str(e)}"
                        )

        return CommandResult(
            success=False,
            message="Command not recognized"
        )



    def wishme(self) -> None:
        """Greet the user based on time of day"""
        hour = datetime.datetime.now().hour
        
        if hour >= 6 and hour < 12:
            greeting = "Good Morning"
        elif hour >= 12 and hour < 18:
            greeting = "Good Afternoon"
        elif hour >= 18 and hour < 24:
            greeting = "Good Evening"
        else:
            greeting = "Good Night"
            
        self.speak(f"{greeting} Sir! Jarvis at your service. How can I help you today?")

    def run(self) -> None:
        """Main loop for running the assistant"""
        self.wishme()
        
        while self.active:
            query = self.listen()
            
            if query == "None":
                continue
                
            result = self.execute_command(query)
            
            if not result.success:
                self.speak(result.message)
            elif result.data:
                self.speak(str(result.data))

    def get_command_history(self, limit: Optional[int] = None) -> List[tuple]:
        """Get recent command history, optionally limited to N entries"""
        history = self.command_history
        if limit:
            history = history[-limit:]
        return history

    def undo_last_command(self) -> CommandResult:
        """Attempt to undo the last executed command"""
        if not self.last_command:
            return CommandResult(
                success=False,
                message="No previous command to undo"
            )
            
        try:
            # Check if command system has undo capability
            for system in [self.productivity_commands, self.system_commands, 
                         self.browser_commands, self.media_commands]:
                if hasattr(system, 'undo_action'):
                    return system.undo_action()
                    
            return CommandResult(
                success=False,
                message="Cannot undo this type of command"
            )
        except Exception as e:
            return CommandResult(
                success=False,
                message=f"Error undoing command: {str(e)}"
            )

    def get_system_status(self) -> Dict[str, Any]:
        """Get current status of the assistant"""
        return {
            'active': self.active,
            'speech_rate': self.engine.getProperty('rate'),
            'volume': self.engine.getProperty('volume'),
            'quiet_mode': self.assistant_commands.quiet_mode,
            'last_command': self.last_command,
            'command_count': len(self.command_history)
        }

if __name__ == "__main__":
    jarvis = Jarvis()
    try:
        jarvis.run()
    except KeyboardInterrupt:
        print("\nJarvis shutting down...")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        # Cleanup
        jarvis.engine.stop()
import datetime
import re
from typing import Dict, List, Callable, Any
import subprocess
import wikipedia
import wolframalpha
import webbrowser as wb
import warnings
import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError
warnings.filterwarnings("ignore", category=UserWarning, module='wikipedia')

class InformationCommands:
    def __init__(self):
        self.wolfram_client = None
        self.chrome_path="c:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe %s"
        self.bravepath='C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'


        # Map functions to their trigger patterns
        self.command_map = {
            self.get_time: [
                r'what(?:\'s| is) the time',
                r'current time',
                r'time now'
            ],

            self.get_date: [
                r'what(?:\'s| is) the date',
                r'current date',
                r'date today',
                r'what day is it',
                r'today\'s date'
            ],

            self.search_wikipedia: [
                r'wiki(pedia)?\s+(.+)',
                r'search wiki(pedia)?\s+(.+)',
                r'look up\s+(.+)\s+on wiki(pedia)?'
            ],

            self.search_youtube: [
                r'youtube\s+(.+)',
                r'search youtube\s+(.+)',
                r'find\s+(.+)\s+on youtube',
                r'play\s+(.+)\s+on youtube'
            ],

            self.google_search: [
                r'search\s+(.+)',
                r'google\s+(.+)',
                r'look up\s+(.+)',
                r'browse\s+(.+)'
            ],

            self.wolfram_search: [
                r'what is\s+(.+)',
                r'who is\s+(.+)',
                r'explain\s+(.+)',
                r'define\s+(.+)',
                r'calculate\s+(.+)'
            ]
        }

    def setup_wolfram(self, app_id: str) -> None:
        """Initialize Wolfram Alpha client with provided API key"""
        self.wolfram_client = wolframalpha.Client(app_id)



    def search_wikipedia(self, command: str) -> str:
        try:
            # Debug print
            print(f"Full command: {command}")
            
            match = re.search(r'wiki(?:pedia)?\s+(.+)', command, re.IGNORECASE)
            if match:
                query = match.group(1).strip()
                print(f"Extracted query: {query}")  # Debug print
                return wikipedia.summary(query, sentences=3)
                
            return "Please specify what to search on Wikipedia"
        except DisambiguationError as e:
            return f"Multiple results found for '{query}'. Options:\n{', '.join(e.options[:5])}"
        except PageError:
            return f"No Wikipedia page found for '{query}'"
        except Exception as e:
            return f"Error searching Wikipedia: {str(e)}"


    def search_youtube(self, command: str) -> str:
        try:
            match = re.search(r'(?:youtube|play|find)\s+(.+?)(?:\s+on youtube)?$', command, re.IGNORECASE)
            if match:
                query = match.group(1).strip()
                url = f"https://www.youtube.com/results?search_query={query}"
                wb.get(self.chrome_path).open(url)
                return f"Searching YouTube for: {query}"
            return "Please specify what to search on YouTube"
        except Exception as e:
            return f"Error with YouTube search: {str(e)}"

    def google_search(self, command: str) -> str:
        try:
            match = re.search(r'(?:search|google|look up|browse)\s+(.+)', command, re.IGNORECASE)
            if match:
                query = match.group(1).strip()
                url = f"https://www.google.com/search?q={query}"
                wb.get(self.chrome_path).open(url)
                return f"Searching Google for: {query}"
            return "Please specify what to search"
        except Exception as e:
            return f"Error with Google search: {str(e)}"

    def wolfram_search(self, command: str) -> str:
        try:
            match = re.search(r'(?:what is|who is|explain|define|calculate)\s+(.+)', command, re.IGNORECASE)
            if match:
                query = match.group(1).strip()
                if not self.wolfram_client:
                    return "Wolfram Alpha client not initialized"
                result = self.wolfram_client.query(query)
                return next(result.results).text
            return "Please specify your question"
        except Exception as e:
            return f"Error with Wolfram Alpha: {str(e)}"

    def get_time(self, command: str = "") -> str:
        return f"Current time: {datetime.datetime.now().strftime('%I:%M %p')}"

    def get_date(self, command: str = "") -> str:
        now = datetime.datetime.now()
        return f"Today is {now.strftime('%B %d, %Y')}"
    
    def execute_command(self, command: str) -> str:
        """Execute the given browser command"""
        command = command.lower()
        
        for func, patterns in self.command_map.items():
            for pattern in patterns:
                if re.search(pattern, command):
                    return func(command)
                
        return "Command not recognized"

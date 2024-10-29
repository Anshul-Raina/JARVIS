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

    def get_time(self, command: str = "") -> str:
        """Get current time in 12-hour format"""
        return datetime.datetime.now().strftime("%I:%M %p")

    def get_date(self, command: str = "") -> Dict[str, int]:
        """Get current date information"""
        now = datetime.datetime.now()
        return {
            'year': now.year,
            'month': now.month,
            'day': now.day
        }



    def search_wikipedia(query: str) -> str:
        """Search Wikipedia and return summary"""
        try:
            # Try to get the summary for the query
            return wikipedia.summary(query, sentences=3)
        except DisambiguationError as e:
            # If there's a disambiguation error, return the options available
            options = "\n".join(e.options[:5])  # Show a few options for brevity
            return f"The term '{query}' is ambiguous. Did you mean:\n{options}"
        except PageError:
            # If the page doesn't exist
            return f"No page found for '{query}'."
        except Exception as e:
            # Handle other generic errors
            return f"Error searching Wikipedia: {str(e)}"


    def search_youtube(self, query: str) -> None:
        """Search or open YouTube"""
        try:
            if 'just open' in query.lower():
                subprocess.Popen([self.brave_path, 'https://www.youtube.com/'])
            else:
                search_query = query.replace('youtube', '').strip()
                url = f"https://www.youtube.com/results?search_query={search_query}"
                wb.get(self.chrome_path).open(url)
        except Exception as e:
            return f"Error with YouTube search: {str(e)}"

    def google_search(self, query: str) -> None:
        """Perform Google search"""
        try:
            search_query = query.replace('search', '').replace('google', '').strip()
            url = f"https://www.google.com/search?q={search_query}"
            wb.get(self.chrome_path).open(url)
        except Exception as e:
            return f"Error with Google search: {str(e)}"

    def wolfram_search(self, query: str) -> str:
        """Search using Wolfram Alpha"""
        if not self.wolfram_client:
            return "Wolfram Alpha client not initialized. Please call setup_wolfram() first."
        
        try:
            result = self.wolfram_client.query(query)
            return next(result.results).text
        except Exception as e:
            return f"Error with Wolfram Alpha search: {str(e)}"

import re  # Added for regular expression searching
import os
import pyautogui
import datetime
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class Reminder:
    text: str
    time: datetime.datetime
    completed: bool = False

class TaskTimer:
    def __init__(self):
        self.start_time: Optional[datetime.datetime] = None
        self.duration: Optional[int] = None
        self.active: bool = False
        
    def start(self, duration_minutes: int) -> str:
        self.start_time = datetime.datetime.now()
        self.duration = duration_minutes
        self.active = True
        return f"Timer started for {duration_minutes} minutes"
        
    def check(self) -> str:
        if not self.active:
            return "No active timer"
        elapsed = datetime.datetime.now() - self.start_time
        remaining = self.duration * 60 - elapsed.total_seconds()
        if remaining <= 0:
            self.active = False
            return "Timer completed!"
        return f"{int(remaining / 60)} minutes {int(remaining % 60)} seconds remaining"
        
    def stop(self) -> str:
        self.active = False
        return "Timer stopped"

class ProductivityCommands:
    def __init__(self):
        self.reminders: List[Reminder] = []
        self.timer = TaskTimer()
        self.vscode_path = 'c:\\Users\\anshu\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe'
        self.notes_file = 'notes.txt'
        self.last_action = None

        # Map functions to trigger patterns
        self.command_map = {
            self.app_operations: [
                r'(open |launch |start )?vs ?code',
                r'type (.*)',
                r'press enter',
                r'undo( that)?'
            ],

            self.note_operations: [
                r'take note(.*)',
                r'write note(.*)',
                r'show notes?',
                r'read notes?'
            ],

            self.reminder_operations: [
                r'add reminder(.*)',
                r'set reminder(.*)',
                r'check (schedule|reminders)',
                r'show (schedule|reminders)',
                r'mark reminder (\d+) (complete|done)'
            ],

            self.timer_operations: [
                r'set timer (\d+)( minutes?)?',
                r'start timer(\d+)( minutes?)?',
                r'stop timer',
                r'check timer'
            ]
        }

    def app_operations(self, command: str) -> str:
        try:
            if 'vs code' in command:
                return self.open_vscode()
            elif 'type' in command:
                text = self._extract_text(command, 'type')
                return self.type_text(text)
            elif 'enter' in command:
                return self.press_enter()
            elif 'undo' in command:
                return self.undo_action()
            return "Invalid application command"
        except Exception as e:
            return f"Error in app operation: {str(e)}"

    def open_vscode(self) -> str:
        try:
            os.startfile(self.vscode_path)
            self.last_action = "Opened VS Code"
            return "VS Code launched successfully"
        except FileNotFoundError:
            return "VS Code not found at specified path"
        except Exception as e:
            return f"Error opening VS Code: {str(e)}"

    def type_text(self, text: str, interval: float = 0.1) -> str:
        try:
            pyautogui.typewrite(text, interval)
            self.last_action = f"Typed: {text}"
            return f"Typed text: {text}"
        except Exception as e:
            return f"Error typing text: {str(e)}"

    def press_enter(self) -> str:
        try:
            pyautogui.press('enter')
            self.last_action = "Pressed Enter"
            return "Enter key pressed"
        except Exception as e:
            return f"Error pressing Enter: {str(e)}"

    def undo_action(self) -> str:
        try:
            pyautogui.hotkey('ctrl', 'z')
            self.last_action = "Undid last action"
            return "Action undone"
        except Exception as e:
            return f"Error undoing action: {str(e)}"

    def note_operations(self, command: str) -> str:
        try:
            if 'take' in command or 'write' in command:
                text = self._extract_text(command, 'note')
                return self.take_note(text)
            elif 'show' in command or 'read' in command:
                return self.show_notes()
            return "Invalid note command"
        except Exception as e:
            return f"Error in note operation: {str(e)}"

    def take_note(self, text: str, include_datetime: bool = True) -> str:
        try:
            mode = 'a' if os.path.exists(self.notes_file) else 'w'
            with open(self.notes_file, mode) as file:
                if include_datetime:
                    timestamp = datetime.datetime.now().strftime("%I:%M %p")
                    file.write(f"\n{timestamp}: {text}")
                else:
                    file.write(f"\n{text}")
            self.last_action = "Saved note"
            return "Note saved successfully"
        except Exception as e:
            return f"Error saving note: {str(e)}"

    def show_notes(self) -> str:
        try:
            if not os.path.exists(self.notes_file):
                return "No notes file exists yet"
            with open(self.notes_file, 'r') as file:
                notes = file.read().strip()
            self.last_action = "Showed notes"
            return notes if notes else "No notes found"
        except Exception as e:
            return f"Error reading notes: {str(e)}"

    def reminder_operations(self, command: str) -> str:
        try:
            if 'add' in command or 'set' in command:
                text = self._extract_text(command, 'reminder')
                return self.add_reminder(text)
            elif 'mark' in command and ('complete' in command or 'done' in command):
                index = int(command.split()[2]) - 1
                return self.mark_reminder_complete(index)
            elif 'check' in command or 'show' in command:
                return self.check_reminders()
            return "Invalid reminder command"
        except Exception as e:
            return f"Error in reminder operation: {str(e)}"

    def add_reminder(self, text: str) -> str:
        self.reminders.append(Reminder(text, datetime.datetime.now()))
        self.last_action = f"Added reminder: {text}"
        return f"Reminder added: {text}"

    def mark_reminder_complete(self, index: int) -> str:
        if 0 <= index < len(self.reminders):
            self.reminders[index].completed = True
            return f"Marked reminder '{self.reminders[index].text}' as complete"
        return "Invalid reminder index"

    def check_reminders(self) -> str:
        if not self.reminders:
            return "No reminders set"
        
        reminder_list = []
        for i, reminder in enumerate(self.reminders, 1):
            status = "✓" if reminder.completed else "○"
            reminder_list.append(
                f"{i}. [{status}] {reminder.text} "
                f"(Set: {reminder.time.strftime('%I:%M %p')})"
            )
        
        self.last_action = "Checked reminders"
        return "\n".join(reminder_list)

    def timer_operations(self, command: str) -> str:
        try:
            if 'set' in command or 'start' in command:
                minutes = int(command.split()[2])  # Extracts number from "set timer 5"
                return self.timer.start(minutes)
            elif 'stop' in command:
                return self.timer.stop()
            elif 'check' in command:
                return self.timer.check()
            return "Invalid timer command"
        except Exception as e:
            return f"Error in timer operation: {str(e)}"

    def _extract_text(self, command: str, keyword: str) -> str:
        """Extract text after a keyword from command"""
        return command.split(keyword, 1)[1].strip() if keyword in command else ""

    def execute_command(self, command: str) -> str:
        command = command.lower()
        
        for func, patterns in self.command_map.items():
            for pattern in patterns:
                if re.search(pattern, command):
                    return func(command)
                
        return "Command not recognized"

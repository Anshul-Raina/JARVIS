import json
import logging
import tkinter as tk
from tkinter import ttk, scrolledtext
import speech_recognition as sr
import threading
import sys
import os
import pyttsx3
import wolframalpha 

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from intents.productivity.productivity_commands import ProductivityCommands
from intents.browser.browser_commands import BrowserCommands
from intents.media.media_commands import MediaCommands
from intents.assistant.assistant_commands import AssistantCommands
from intents.security.security_commands import SecurityCommands
from intents.system.system_commands import SystemCommands
from intents.information.information_commands import InformationCommands

class VoiceAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jarvis Voice Assistant")
        self.root.geometry("800x600")
        
        # Initialize text-to-speech engine
        self.engine = None  # We'll create engines per request
        self.current_engine = None  # Track current speaking engine
        
        # Initialize speech control flags
        self.is_speaking = False
        self.stop_speaking = threading.Event()
        self.speech_lock = threading.Lock()
        
        # Initialize command handlers
        self.productivity = ProductivityCommands()
        self.browser = BrowserCommands()
        self.media = MediaCommands()
        self.assistant = AssistantCommands()
        self.security = SecurityCommands()
        self.system = SystemCommands()
        self.information = InformationCommands()
        self.information.setup_wolfram("LQP4EK-UU2GLWH4GH")
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        
        self.setup_gui()
        self.is_processing = False
        self.processing_lock = threading.Lock()
    

    def speak(self, text):
        """Speak the given text using text-to-speech"""
        with self.speech_lock:
            # Force stop any current speech
            if self.is_speaking and self.current_engine:
                self.stop_speaking.set()
                try:
                    self.current_engine.stop()
                except:
                    pass
                self.is_speaking = False
            
            # Start new speech
            self.stop_speaking.clear()
            threading.Thread(target=self._speak_thread, args=(text,), daemon=True).start()

    def _speak_thread(self, text):
        """Handle text-to-speech in a separate thread with interruption support"""
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.9)
            
            with self.speech_lock:
                if self.current_engine:
                    try:
                        self.current_engine.endLoop()
                        del self.current_engine
                    except:
                        pass
                self.current_engine = engine
                self.is_speaking = True
            
            if not self.stop_speaking.is_set():
                engine.connect('started-utterance', self.check_interrupt)
                engine.say(text)
                engine.startLoop(False)
                
                while engine.iterate() and not self.stop_speaking.is_set():
                    pass
                
                engine.endLoop()
            
        except Exception as e:
            logging.error(f"TTS error: {str(e)}")
            self.update_output("Error: Could not generate speech")
        finally:
            with self.speech_lock:
                self.is_speaking = False
                self.current_engine = None
                self.stop_speaking.clear()
            try:
                engine.endLoop()
                del engine
            except:
                pass


    def check_interrupt(self, name, completed):
        """Check if speech should be interrupted"""
        if self.stop_speaking.is_set():
            try:
                self.current_engine.endLoop()
            except:
                pass
            return False
        return True

    def interrupt_current_operations(self):
        """Interrupt any ongoing speech or processing immediately"""
        # Stop any ongoing speech immediately
        with self.speech_lock:
            if self.is_speaking and self.current_engine:
                self.stop_speaking.set()  # Signal to stop speaking
                try:
                    self.current_engine.endLoop()  # Forcefully end the TTS loop
                    del self.current_engine  # Clean up the engine instance
                except Exception as e:
                    logging.error(f"Error stopping TTS engine: {str(e)}")
                self.is_speaking = False
                self.current_engine = None
                self.update_output("Interrupted previous speech for new command")

        # Reset processing immediately, even if the previous task was ongoing
        with self.processing_lock:
            if self.is_processing:
                self.is_processing = False  # Force reset processing flag
                self.update_output("Previous processing forcefully stopped for new command")

                
    def listen_for_commands(self):
        while self.is_listening:
            try:
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    self.update_output("Listening...")
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                
                text = self.recognizer.recognize_google(audio).lower()
                self.command_label.config(text=f"Last Command: {text}")
                
                # Immediately stop any speech as soon as we detect a command
                if self.is_speaking:
                    with self.speech_lock:
                        if self.current_engine:
                            self.stop_speaking.set()
                            try:
                                self.current_engine.endLoop()
                                del self.current_engine
                            except:
                                pass
                            self.is_speaking = False
                            self.current_engine = None
                            self.update_output("Stopped speaking for new command")
                
                # Now process the new command
                self.process_command(text)
                
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                message = f"Could not request results: {str(e)}"
                self.update_output(message)
            except Exception as e:
                message = f"Error: {str(e)}"
                self.update_output(message)

        

                
    def setup_gui(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weight
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Add text area for output
        self.output_area = scrolledtext.ScrolledText(main_frame, height=20, width=70)
        self.output_area.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Control frame for buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=1, column=0, columnspan=3, pady=10)
        
        # Add buttons
        self.listen_button = ttk.Button(control_frame, text="Start Listening", 
                                      command=self.toggle_listening, width=20)
        self.listen_button.grid(row=0, column=0, padx=5)
        
        clear_button = ttk.Button(control_frame, text="Clear Output", 
                                command=self.clear_output, width=20)
        clear_button.grid(row=0, column=1, padx=5)
        
        quit_button = ttk.Button(control_frame, text="Quit", 
                               command=self.root.quit, width=20)
        quit_button.grid(row=0, column=2, padx=5)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Status: Ready", 
                                    font=('Arial', 10))
        self.status_label.grid(row=2, column=0, columnspan=3, pady=5)
        
        # Command history label
        self.command_label = ttk.Label(main_frame, text="Last Command: None", 
                                     font=('Arial', 10))
        self.command_label.grid(row=3, column=0, columnspan=3, pady=5)
    
    def clear_output(self):
        self.output_area.delete(1.0, tk.END)
        self.update_output("Output cleared")
        self.speak("Output cleared")
    
    def toggle_listening(self):
        if not self.is_listening:
            self.is_listening = True
            self.listen_button.config(text="Stop Listening")
            self.status_label.config(text="Status: Listening...")
            self.speak("Listening activated")
            threading.Thread(target=self.listen_for_commands, daemon=True).start()
        else:
            self.is_listening = False
            self.listen_button.config(text="Start Listening")
            self.status_label.config(text="Status: Ready")
            self.speak("Listening deactivated")
            
    def update_output(self, message):
        """Update the output text area with the given message"""
        self.output_area.insert(tk.END, f"{message}\n")
        self.output_area.see(tk.END)  # Auto-scroll to the end
        
   
    
    def process_command(self, text):
        """Process voice commands with immediate interruption of previous operations"""
        self.update_output(f"Processing command: {text}")

        try:
            intent_handlers = [
                self.system,
                self.security,
                self.productivity,
                self.browser,
                self.media,
                self.assistant,
                self.information
            ]

            for handler in intent_handlers:
                try:
                    response = handler.execute_command(text)

                    if isinstance(response, str) and response.startswith('{'): 
                        try:
                            json.loads(response)
                        except json.JSONDecodeError:
                            response = "Error: Invalid response format"

                    if response != "Command not recognized":
                        self.update_output(str(response))
                        # Only speak if we haven't been interrupted
                        if not self.stop_speaking.is_set():
                            self.speak(str(response))
                        return

                except Exception as handler_error:
                    logging.error(f"Handler error: {handler_error}")
                    continue

            message = "Command not recognized"
            self.update_output(message)
            if not self.stop_speaking.is_set():
                self.speak(message)

        except Exception as e:
            error_msg = f"Error processing command: {str(e)}"
            self.update_output(error_msg)
            if not self.stop_speaking.is_set():
                self.speak("Error processing command")
            return error_msg


    

def main():
    # Set up the main window
    root = tk.Tk()
    root.title("Jarvis Voice Assistant")
    
    # Set theme (if available)
    try:
        root.tk.call("source", "azure.tcl")
        root.tk.call("set_theme", "dark")
    except:
        pass
    
    # Create and run the application
    app = VoiceAssistantGUI(root)
    
    # Set window icon (if available)
    try:
        root.iconbitmap("jarvis_icon.ico")
    except:
        pass
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
import sys
import cv2 
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageSequence
import threading
import time
import os
from pathlib import Path
from typing import Optional
import speech_recognition as sr
import pyttsx3
from jarvis import Jarvis

def check_opencv_face():
    """Check if OpenCV face module is available and install if needed"""
    try:
        import cv2
        return cv2.face.LBPHFaceRecognizer_create()
    except AttributeError:
        print("OpenCV face recognition module not found. Please install opencv-contrib-python.")
        import subprocess
        try:
            subprocess.check_call(['pip', 'install', 'opencv-contrib-python'])
            import cv2  # Retry importing cv2 after installation
            return cv2.face.LBPHFaceRecognizer_create()
        except Exception as e:
            print(f"Error installing package: {e}")
            print("Please manually install using: pip install opencv-contrib-python")
            return None


class JarvisInterface(tk.Frame):
    """GUI interface for Jarvis post-authentication"""
    def __init__(self, master, jarvis_instance):
        super().__init__(master)
        self.master = master
        self.jarvis = jarvis_instance
        self.listening = False
        self.setup_gui()

    def setup_gui(self):
        """Setup the GUI components"""
        # Main container
        self.container = ttk.Frame(self)
        self.container.pack(fill='both', expand=True)

        # Status label
        self.status_label = ttk.Label(
            self.container,
            text="Jarvis Ready",
            font=('Arial', 14),
            background='black',
            foreground='#00ff00'
        )
        self.status_label.pack(pady=10)

        # Command button
        self.command_button = ttk.Button(
            self.container,
            text="🎤 Start Listening",
            command=self.toggle_listening,
            style='Accent.TButton'
        )
        self.command_button.pack(pady=20)

        # Command history
        self.history_frame = ttk.Frame(self.container)
        self.history_frame.pack(fill='both', expand=True, padx=20, pady=10)

        self.history_label = ttk.Label(
            self.history_frame,
            text="Command History:",
            font=('Arial', 12)
        )
        self.history_label.pack(anchor='w')

        self.history_text = tk.Text(
            self.history_frame,
            height=10,
            width=50,
            font=('Courier', 10),
            bg='black',
            fg='#00ff00'
        )
        self.history_text.pack(fill='both', expand=True)

        # Create custom style for the button
        style = ttk.Style()
        style.configure(
            'Accent.TButton',
            font=('Arial', 12),
            padding=10
        )

        # Initialize text-to-speech in a separate thread
        self.tts_thread = None
        
    def speak_async(self, text):
        """Handle speech in a separate thread to prevent GUI freezing"""
        if self.tts_thread and self.tts_thread.is_alive():
            self.jarvis.engine.stop()  # Stop any ongoing speech
            self.tts_thread.join()
            
        def speak_text():
            try:
                self.jarvis.engine.say(text)
                self.jarvis.engine.runAndWait()
            except Exception as e:
                print(f"Speech error: {e}")
                
        self.tts_thread = threading.Thread(target=speak_text)
        self.tts_thread.start()
    
    def toggle_listening(self):
        """Toggle the listening state"""
        if self.listening:
            self.listening = False
            self.command_button.configure(text="🎤 Start Listening")
            self.status_label.configure(text="Jarvis Ready")
            self.speak_async("Listening stopped")
        else:
            self.listening = True
            self.command_button.configure(text="⏹ Stop Listening")
            self.status_label.configure(text="Listening...")
            self.speak_async("Listening started")
            threading.Thread(target=self.listen_for_commands, daemon=True).start()

    def listen_for_commands(self):
        """Listen for and process voice commands"""
        while self.listening:
            query = self.jarvis.listen()
            if query != "None" and self.listening:
                self.status_label.configure(text="Processing command...")
                result = self.jarvis.execute_command(query)
                
                # Update history
                timestamp = time.strftime("%H:%M:%S")
                self.history_text.insert('1.0', f"[{timestamp}] User: {query}\n")
                
                # Only add Jarvis response if there's a meaningful message
                if result.message and not result.message.startswith("Command executed successfully"):
                    self.history_text.insert('1.0', f"[{timestamp}] Jarvis: {result.message}\n")
                    # Speak the response
                    self.speak_async(result.message)
                elif not result.success:
                    # Always speak and show error messages
                    self.history_text.insert('1.0', f"[{timestamp}] Jarvis: {result.message}\n")
                    self.speak_async(result.message)
                
                self.history_text.insert('1.0', "-" * 50 + "\n")
                self.status_label.configure(text="Jarvis Ready")

    def cleanup(self):
        """Clean up resources before closing"""
        if self.tts_thread and self.tts_thread.is_alive():
            self.jarvis.engine.stop()
            self.tts_thread.join()
class JarvisAuthenticationSystem:
    def __init__(self, cascade_path='haarcascade_frontalface_default.xml'):
        # Initialize face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + cascade_path)
        
        # Initialize face recognizer
        self.face_recognizer = check_opencv_face()
        if not self.face_recognizer:
            messagebox.showerror("Error", "Failed to initialize face recognition. Please install opencv-contrib-python")
            sys.exit(1)
            
        self.authenticated = False
        self.training_faces = []
        self.training_labels = []
        self.user_id = 1
        
        # Initialize GUI
        self.root = tk.Tk()
        self.root.title("Jarvis System")
        self.root.geometry("800x600")
        self.root.configure(bg='black')
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)
        
        # Create canvas for GIF display
        self.canvas = tk.Canvas(self.main_frame, width=800, height=600)
        self.canvas.pack(fill='both', expand=True)
        
        # Create overlay frame for camera feed
        self.overlay_frame = ttk.Frame(self.main_frame)
        self.overlay_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Camera feed label
        self.camera_label = ttk.Label(self.overlay_frame)
        self.camera_label.pack()
        
        # Status label
        self.status_label = ttk.Label(
            self.overlay_frame,
            text="Initializing...",
            font=('Arial', 12),
            background='black',
            foreground='#00ff00'
        )
        self.status_label.pack(pady=10)

        try:
            # Load GIFs
            self.auth_gif = self.load_gif("jarvis_authentication_gui.gif")
            self.main_gif = self.load_gif("NUxj.gif")
            if not self.main_gif:
                raise FileNotFoundError("NUxj.gif not found or failed to load")
            self.current_frames = self.auth_gif
            self.current_frame = 0
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load GIF files: {str(e)}")
            sys.exit(1)
        
        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Failed to open camera")
            sys.exit(1)
        
        # Create data directory if it doesn't exist
        self.data_dir = Path("face_data")
        self.data_dir.mkdir(exist_ok=True)
        
        # Load existing face data if available
        self.load_face_data()
        
        # Initialize Jarvis instance
        self.jarvis = None
        self.jarvis_interface = None

    def load_gif(self, gif_path):
        """Load a GIF file and return a list of frames as ImageTk.PhotoImage objects."""
        try:
            # Verify file exists
            if not os.path.exists(gif_path):
                print(f"GIF file not found: {gif_path}")
                return []
                
            print(f"Loading GIF: {gif_path}")
            gif_image = Image.open(gif_path)
            frames = []
            
            # Get gif size
            gif_width, gif_height = gif_image.size
            print(f"GIF dimensions: {gif_width}x{gif_height}")
            
            # Calculate scaling factors to fit 800x600 canvas while maintaining aspect ratio
            scale = min(800/gif_width, 600/gif_height)
            new_width = int(gif_width * scale)
            new_height = int(gif_height * scale)
            
            for frame in ImageSequence.Iterator(gif_image):
                # Convert and resize frame
                frame = frame.convert("RGBA")
                frame = frame.resize((new_width, new_height), Image.Resampling.LANCZOS)
                frames.append(ImageTk.PhotoImage(frame))
                
            print(f"Loaded {len(frames)} frames")
            return frames
            
        except Exception as e:
            print(f"Error loading GIF {gif_path}: {str(e)}")
            return []
        
    def update_gif(self):
        """Update the current frame of the GIF on the canvas."""
        if not hasattr(self, 'canvas') or not self.canvas.winfo_exists():
            return
        
        if self.current_frames:
            try:
                frame = self.current_frames[self.current_frame]
                self.canvas.delete("all")  # Clear previous frame
                
                # Calculate center position
                canvas_width = self.canvas.winfo_width()
                canvas_height = self.canvas.winfo_height()
                frame_width = frame.width()
                frame_height = frame.height()
                
                x = (canvas_width - frame_width) // 2
                y = (canvas_height - frame_height) // 2
                
                # Draw frame centered
                self.canvas.create_image(x + frame_width//2, y + frame_height//2, 
                                       image=frame, anchor='center')
                
                self.current_frame = (self.current_frame + 1) % len(self.current_frames)
                
            except Exception as e:
                print(f"Error updating GIF frame: {str(e)}")
            
        self.root.after(50, self.update_gif)  # Increased animation speed


    def capture_face(self, frame):
        """Detect and return face from frame"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            return gray[y:y+h, x:x+w], faces[0]
        return None, None

    def train_face(self):
        """Capture and train face data"""
        self.status_label.config(text="Training face... Please look at the camera")
        
        face_samples = []
        for _ in range(30):  # Capture 30 samples
            ret, frame = self.cap.read()
            if ret:
                face, _ = self.capture_face(frame)
                if face is not None:
                    face_samples.append(face)
                    time.sleep(0.1)
        
        if face_samples:
            # Save face samples
            for i, face in enumerate(face_samples):
                cv2.imwrite(str(self.data_dir / f"user_{self.user_id}_sample_{i}.jpg"), face)
            
            # Update training data
            self.training_faces.extend(face_samples)
            self.training_labels.extend([self.user_id] * len(face_samples))
            
            # Train recognizer
            self.face_recognizer.train(self.training_faces, 
                                     np.array(self.training_labels))
            
            self.status_label.config(text="Training complete!")
            return True
        
        self.status_label.config(text="Training failed. Please try again.")
        return False

    def verify_face(self, face):
        """Verify captured face against trained data"""
        try:
            label, confidence = self.face_recognizer.predict(face)
            return confidence < 70  # Threshold for recognition confidence
        except:
            return False

    def load_face_data(self):
        """Load existing face data from directory"""
        if self.data_dir.exists():
            face_files = list(self.data_dir.glob("*.jpg"))
            if face_files:
                for file in face_files:
                    face = cv2.imread(str(file), cv2.IMREAD_GRAYSCALE)
                    self.training_faces.append(face)
                    self.training_labels.append(self.user_id)
                
                self.face_recognizer.train(self.training_faces, 
                                         np.array(self.training_labels))
                return True
        return False

    def switch_to_jarvis_interface(self):
        """Switch to Jarvis interface after authentication"""
        # Clear current widgets while preserving the canvas
        for widget in self.main_frame.winfo_children():
            if widget != self.canvas:
                widget.destroy()

        # Switch to main GIF
        print("Switching to main GIF animation")
        self.current_frames = self.main_gif
        self.current_frame = 0

        # Initialize Jarvis
        from jarvis import Jarvis
        self.jarvis = Jarvis()

        # Create and show Jarvis interface
        self.jarvis_interface = JarvisInterface(self.main_frame, self.jarvis)
        self.jarvis_interface.pack(fill='both', expand=True)

        # Update window
        self.root.update()

    def update_camera(self):
        """Update camera feed and handle face recognition"""
        ret, frame = self.cap.read()
        if ret:
            face, face_coords = self.capture_face(frame)
            
            if face is not None:
                (x, y, w, h) = face_coords
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                if not self.authenticated:
                    if not self.training_faces:
                        if self.train_face():
                            self.status_label.config(text="Face trained! Please look at the camera to verify.")
                    else:
                        if self.verify_face(face):
                            self.authenticated = True
                            self.status_label.config(text="Authentication successful!")
                            self.current_frames = self.main_gif
                            self.current_frame = 0
                            self.cap.release()
                            cv2.destroyAllWindows()
                            self.switch_to_jarvis_interface()
                            return
            
            # Convert frame for display
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = img.resize((320, 240))
            img = ImageTk.PhotoImage(image=img)
            
            self.camera_label.config(image=img)
            self.camera_label.image = img
        
        if not self.authenticated:
            self.root.after(10, self.update_camera)

    def run(self):
        """Run the authentication system"""
        self.update_gif()
        self.update_camera()
        self.root.mainloop()

    def cleanup(self):
        """Clean up resources"""
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        if self.jarvis and hasattr(self.jarvis, 'engine'):
            self.jarvis.engine.stop()
        self.root.quit()

if __name__ == "__main__":
    try:
        import cv2
        # Confirm OpenCV version
        cv_version = cv2.__version__
        print(f"OpenCV version: {cv_version}")

        # Initialize the authentication system
        auth_system = JarvisAuthenticationSystem()
        auth_system.run()
        
    except ImportError:
        print("OpenCV not found. Installing required packages...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'opencv-contrib-python'])
        print("Installation complete. Please restart the program.")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        if 'auth_system' in locals():
            auth_system.cleanup()

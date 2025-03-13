import tkinter as tk
from tkinter import messagebox
import webbrowser
import subprocess
import sys
import os
import random
import math
import threading
import tempfile
from pytube import YouTube
import pygame

class Ball:
    def __init__(self, canvas, color, size, width, height):
        self.canvas = canvas
        self.color = color
        self.size = size
        # Random starting position using actual window dimensions
        self.x = random.randint(size, width - size)
        self.y = random.randint(size, height - size)
        # Random velocity (non-zero to ensure movement)
        self.dx = random.uniform(-2, 2)
        while -0.5 < self.dx < 0.5:  # Ensure non-zero velocity
            self.dx = random.uniform(-2, 2)
            
        self.dy = random.uniform(-2, 2)
        while -0.5 < self.dy < 0.5:  # Ensure non-zero velocity
            self.dy = random.uniform(-2, 2)
            
        # Create the ball on canvas
        self.ball = canvas.create_oval(
            self.x - self.size, self.y - self.size,
            self.x + self.size, self.y + self.size,
            fill=self.color, outline=""
        )
    
    def move(self):
        # Update position
        self.x += self.dx
        self.y += self.dy
        
        # Bounce off edges
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if self.x - self.size <= 0:
            self.dx = abs(self.dx)  # Move right
            self.x = self.size  # Prevent sticking to edge
        elif self.x + self.size >= width:
            self.dx = -abs(self.dx)  # Move left
            self.x = width - self.size  # Prevent sticking to edge
            
        if self.y - self.size <= 0:
            self.dy = abs(self.dy)  # Move down
            self.y = self.size  # Prevent sticking to edge
        elif self.y + self.size >= height:
            self.dy = -abs(self.dy)  # Move up
            self.y = height - self.size  # Prevent sticking to edge
        
        # Move the ball on canvas by calculating the difference
        current_pos = self.canvas.coords(self.ball)
        if len(current_pos) == 4:  # Make sure the ball exists
            current_x = (current_pos[0] + current_pos[2]) / 2
            current_y = (current_pos[1] + current_pos[3]) / 2
            self.canvas.move(self.ball, self.x - current_x, self.y - current_y)

def download_and_play_audio():
    """Download and play the background audio"""
    try:
        # YouTube video URL
        url = "https://www.youtube.com/watch?v=YAgJ9XugGBo"
        
        # Create a temporary directory for the audio
        temp_dir = tempfile.gettempdir()
        audio_path = os.path.join(temp_dir, "background_audio.mp4")
        
        # Download the video if it hasn't been downloaded
        if not os.path.exists(audio_path):
            yt = YouTube(url)
            # Get the audio stream
            audio_stream = yt.streams.filter(only_audio=True).first()
            audio_stream.download(output_path=temp_dir, filename="background_audio.mp4")
        
        # Initialize pygame mixer
        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely
        
    except Exception as e:
        print(f"Error setting up audio: {e}")

def create_response(choice):
    """Handle button clicks and show custom responses based on the choice"""
    responses = {
        "Yes": "Good boy",
        "No": "Bad boy",
        "Maybe": "kys",
        "Bleh": "Me too"
    }
    
    messagebox.showinfo("Response", responses[choice])

def open_rickroll():
    """Open the rickroll YouTube link"""
    webbrowser.open("https://www.youtube.com/watch?v=xvFZjo5PgG0")

def run_powershell_admin():
    """Attempt to open PowerShell as admin and run wininit"""
    try:
        if sys.platform == 'win32':
            # Command to run PowerShell as admin with wininit
            cmd = 'powershell.exe -Command "Start-Process powershell -ArgumentList \'-NoProfile -Command wininit\' -Verb RunAs"'
            subprocess.Popen(cmd, shell=True)
    except Exception as e:
        pass

def main():
    # Create the main window
    root = tk.Tk()
    root.title("Option Selector")
    
    # Start downloading and playing the audio in a separate thread
    audio_thread = threading.Thread(target=download_and_play_audio, daemon=True)
    audio_thread.start()
    
    # Add a function to handle cleanup when closing the window
    def on_closing():
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except:
            pass
        root.destroy()
    
    # Bind the closing function to the window's close button
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Make the window fullscreen
    root.attributes('-fullscreen', True)
    
    # Create a canvas for the background with balls
    background_canvas = tk.Canvas(root, bg="black", highlightthickness=0)
    background_canvas.pack(fill=tk.BOTH, expand=True)
    
    # Create a transparent frame for content
    content_frame = tk.Frame(root, bg="")
    content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    # Create a header label with the text "Choose below"
    header = tk.Label(
        content_frame, 
        text="Choose below", 
        font=("Arial", 24),
        bg="black",
        fg="white"
    )
    header.pack(pady=40)
    
    # Define button styles - much bigger buttons
    button_width = 30
    button_height = 3
    button_font = ("Arial", 18)
    button_pady = 15
    
    # Create a frame to center the buttons
    button_frame = tk.Frame(content_frame, bg="black")
    button_frame.pack(expand=True)
    
    # Create the four option buttons
    yes_button = tk.Button(
        button_frame, 
        text="1. Yes", 
        width=button_width, 
        height=button_height,
        font=button_font,
        command=lambda: create_response("Yes")
    )
    yes_button.pack(pady=button_pady)
    
    no_button = tk.Button(
        button_frame, 
        text="2. No", 
        width=button_width, 
        height=button_height,
        font=button_font,
        command=lambda: create_response("No")
    )
    no_button.pack(pady=button_pady)
    
    maybe_button = tk.Button(
        button_frame, 
        text="3. Maybe", 
        width=button_width, 
        height=button_height,
        font=button_font,
        command=lambda: create_response("Maybe")
    )
    maybe_button.pack(pady=button_pady)
    
    bleh_button = tk.Button(
        button_frame, 
        text="4. Bleh", 
        width=button_width, 
        height=button_height,
        font=button_font,
        command=lambda: create_response("Bleh")
    )
    bleh_button.pack(pady=button_pady)
    
    # Add the Rickroll button
    rickroll_button = tk.Button(
        button_frame, 
        text="Rickroll", 
        width=button_width, 
        height=button_height,
        font=button_font,
        bg="red",
        fg="white",
        command=open_rickroll
    )
    rickroll_button.pack(pady=button_pady)
    
    # Add the sad button
    sad_button = tk.Button(
        button_frame, 
        text="5. :(", 
        width=button_width, 
        height=button_height,
        font=button_font,
        bg="gray",
        fg="white",
        command=run_powershell_admin
    )
    sad_button.pack(pady=button_pady)
    
    # Add an exit button to allow closing the fullscreen window
    exit_button = tk.Button(
        root,
        text="Exit",
        font=("Arial", 14),
        bg="darkred",
        fg="white",
        command=on_closing,
        width=10,
        height=1
    )
    exit_button.place(relx=0.5, rely=0.95, anchor=tk.CENTER)
    
    # Wait for the window to be drawn and get actual dimensions
    def initialize_balls():
        # Get actual window dimensions
        width = background_canvas.winfo_width()
        height = background_canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            # Window not fully drawn yet, wait a bit more
            root.after(100, initialize_balls)
            return
            
        # Create balls with actual dimensions
        balls = []
        for _ in range(15):  # Create 15 white balls
            balls.append(Ball(background_canvas, "white", random.randint(10, 30), width, height))
        
        for _ in range(15):  # Create 15 purple balls
            balls.append(Ball(background_canvas, "purple", random.randint(10, 30), width, height))
        
        # Function to animate the balls
        def animate_balls():
            for ball in balls:
                ball.move()
            root.after(30, animate_balls)  # Update every 30ms
        
        # Start animation
        animate_balls()
    
    # Start ball initialization after a short delay to ensure window is drawn
    root.after(200, initialize_balls)
    
    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()

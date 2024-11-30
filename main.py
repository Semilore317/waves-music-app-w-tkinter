import tkinter as tk
from tkinter import filedialog
import pygame
import os


class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Waves")
        self.root.geometry("600x400")
        self.root.config(bg="#1DB954")  # Green theme

        # Initialize pygame mixer for audio
        pygame.mixer.init()

        # Track Information
        self.track = None
        self.is_playing = False

        # UI Elements
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title_label = tk.Label(self.root, text="Waves", font=("Arial", 24), bg="#1DB954", fg="white")
        title_label.pack(pady=10)

        # Song Name Label
        self.song_name_label = tk.Label(self.root, text="No song selected", font=("Arial", 14), bg="#1DB954",
                                        fg="white")
        self.song_name_label.pack(pady=5)

        # Play/Pause Button
        self.play_button = tk.Button(self.root, text="Play", command=self.toggle_play, font=("Arial", 12), bg="#1DB954",
                                     fg="white")
        self.play_button.pack(pady=5)

        # Open File Button
        self.open_button = tk.Button(self.root, text="Open", command=self.open_file, font=("Arial", 12), bg="#1DB954",
                                     fg="white")
        self.open_button.pack(pady=5)

        # Volume Control
        self.volume_label = tk.Label(self.root, text="Volume", font=("Arial", 12), bg="#1DB954", fg="white")
        self.volume_label.pack(pady=5)

        self.volume_scale = tk.Scale(self.root, from_=0, to=1, orient="horizontal", resolution=0.01,
                                     command=self.set_volume, bg="#1DB954", fg="white")
        self.volume_scale.set(0.5)  # Default volume
        self.volume_scale.pack(pady=5)

        # Stop Button
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_music, font=("Arial", 12), bg="#1DB954",
                                     fg="white")
        self.stop_button.pack(pady=5)

    def toggle_play(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.play_button.config(text="Play")
        else:
            if self.track:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.load(self.track)
                pygame.mixer.music.play()
            self.play_button.config(text="Pause")
        self.is_playing = not self.is_playing

    def stop_music(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.play_button.config(text="Play")

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav;*.ogg")])
        if file_path:
            self.track = file_path
            self.song_name_label.config(text=os.path.basename(file_path))
            if self.is_playing:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(self.track)
                pygame.mixer.music.play()
                self.play_button.config(text="Pause")
                self.is_playing = True

    def set_volume(self, val):
        pygame.mixer.music.set_volume(float(val))


# Create main window
root = tk.Tk()

# Initialize the music player
player = MusicPlayer(root)

# Start the main loop
root.mainloop()
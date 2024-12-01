import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pygame

# Initialize pygame mixer
pygame.mixer.init()

class AudaciousLite:
    def __init__(self, root):
        self.root = root
        self.root.title("Audacious Lite")
        self.root.geometry("900x600")
        self.root.configure(bg="#1b5e20")

        self.current_track_index = None
        self.playlist = []
        self.is_playing = False

        # Header
        self.header = tk.Frame(self.root, bg="#2e7d32", height=60)
        self.header.pack(side="top", fill="x")
        tk.Label(
            self.header, text="Audacious Lite", font=("Arial", 24, "bold"), bg="#2e7d32", fg="white"
        ).pack(pady=10)

        # Playlist section
        self.playlist_frame = tk.Frame(self.root, bg="#1b5e20")
        self.playlist_frame.pack(side="left", fill="both", padx=10, pady=10)

        tk.Label(self.playlist_frame, text="Playlist", bg="#1b5e20", fg="white", font=("Arial", 14)).pack(anchor="w")

        self.playlist_box = tk.Listbox(
            self.playlist_frame, bg="#4caf50", fg="white", font=("Arial", 12), selectbackground="#388e3c", height=25
        )
        self.playlist_box.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Playlist buttons
        self.playlist_controls = tk.Frame(self.playlist_frame, bg="#1b5e20")
        self.playlist_controls.pack(fill="x")
        ttk.Button(self.playlist_controls, text="Add Tracks", command=self.add_tracks).pack(side="left", padx=5)
        ttk.Button(self.playlist_controls, text="Remove", command=self.remove_track).pack(side="left", padx=5)
        ttk.Button(self.playlist_controls, text="Clear Playlist", command=self.clear_playlist).pack(side="left", padx=5)

        # Playback controls
        self.controls_frame = tk.Frame(self.root, bg="#2e7d32", height=80)
        self.controls_frame.pack(side="bottom", fill="x", pady=10)

        self.play_button = ttk.Button(self.controls_frame, text="Play", command=self.play_track)
        self.play_button.pack(side="left", padx=10)

        self.pause_button = ttk.Button(self.controls_frame, text="Pause", command=self.pause_track)
        self.pause_button.pack(side="left", padx=10)

        self.stop_button = ttk.Button(self.controls_frame, text="Stop", command=self.stop_track)
        self.stop_button.pack(side="left", padx=10)

        self.prev_button = ttk.Button(self.controls_frame, text="Prev", command=self.prev_track)
        self.prev_button.pack(side="left", padx=10)

        self.next_button = ttk.Button(self.controls_frame, text="Next", command=self.next_track)
        self.next_button.pack(side="left", padx=10)

        # Volume slider
        self.volume_label = tk.Label(self.controls_frame, text="Volume", bg="#2e7d32", fg="white")
        self.volume_label.pack(side="left", padx=5)
        self.volume_slider = ttk.Scale(self.controls_frame, from_=0, to=100, orient="horizontal", command=self.set_volume)
        self.volume_slider.set(50)
        self.volume_slider.pack(side="left", padx=5)

        # Equalizer (placeholder for simplicity)
        self.eq_frame = tk.Frame(self.root, bg="#1b5e20", height=100)
        self.eq_frame.pack(side="right", fill="y", padx=10, pady=10)
        tk.Label(self.eq_frame, text="Equalizer", bg="#1b5e20", fg="white", font=("Arial", 14)).pack(anchor="w")
        for freq in ["60Hz", "170Hz", "310Hz", "600Hz", "1kHz", "3kHz", "6kHz", "12kHz", "14kHz", "16kHz"]:
            tk.Scale(self.eq_frame, from_=-10, to=10, orient="vertical", label=freq, bg="#1b5e20", fg="white").pack(
                side="left", padx=5
            )

    def add_tracks(self):
        files = filedialog.askopenfilenames(
            title="Select Music Files", filetypes=(("Audio Files", "*.mp3;*.wav;*.ogg"),)
        )
        for file in files:
            self.playlist.append(file)
            self.playlist_box.insert(tk.END, os.path.basename(file))

    def remove_track(self):
        selected = self.playlist_box.curselection()
        if selected:
            index = selected[0]
            self.playlist.pop(index)
            self.playlist_box.delete(index)

    def clear_playlist(self):
        self.playlist = []
        self.playlist_box.delete(0, tk.END)

    def play_track(self):
        selected = self.playlist_box.curselection()
        if selected:
            index = selected[0]
            self.current_track_index = index
            track = self.playlist[index]
            pygame.mixer.music.load(track)
            pygame.mixer.music.play()
            self.is_playing = True

    def pause_track(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
        else:
            pygame.mixer.music.unpause()
            self.is_playing = True

    def stop_track(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def prev_track(self):
        if self.current_track_index is not None and self.current_track_index > 0:
            self.current_track_index -= 1
            self.play_track()

    def next_track(self):
        if self.current_track_index is not None and self.current_track_index < len(self.playlist) - 1:
            self.current_track_index += 1
            self.play_track()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume) / 100)


if __name__ == "__main__":
    root = tk.Tk()
    app = AudaciousLite(root)
    root.mainloop()

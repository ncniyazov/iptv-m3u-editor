import os
import errno
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import scrolledtext


class PlaylistSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Playlist Splitter by © ncniyazov")

        self.playlist_file_path = tk.StringVar()
        self.chunk_size = tk.IntVar(value=3)
        self.log_text = ""

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Select Playlist File:").pack()
        tk.Button(self.root, text="Browse",
                  command=self.browse_playlist_file).pack()

        tk.Label(self.root, text="Chunk Size:").pack()
        tk.Entry(self.root, textvariable=self.chunk_size).pack()

        self.log_widget = scrolledtext.ScrolledText(
            self.root, height=10, width=50)
        self.log_widget.pack()

        self.progress_bar = ttk.Progressbar(
            self.root, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.pack()

        tk.Button(self.root, text="Export",
                  command=self.export_channels).pack()

    def browse_playlist_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("M3U Files", "*.m3u*")])
        if file_path:
            self.playlist_file_path.set(file_path)

    def log(self, message):
        self.log_text += message + "\n"
        self.log_widget.delete("1.0", tk.END)
        self.log_widget.insert(tk.END, self.log_text)
        self.log_widget.see(tk.END)

    def update_progress(self, value):
        self.progress_bar["value"] = value
        self.root.update_idletasks()

    def split_channels(self, playlist_file):
        playlist = []
        with open(playlist_file, "r", encoding="utf-8") as f:
            for line in f:
                playlist.append(line)

        # chunk
        chunk_size = self.chunk_size.get()

        chunks = [playlist[i:i + chunk_size]
                for i in range(1, len(playlist), chunk_size)]
        result_list = []

        for chunk in chunks:
            result_list.append(chunk)
        # print (result_list)

        sd_channels = []
        hd_channels = []

        for i in result_list:
            channel = i[0]
            if "HD" in channel or "4K" in channel or "4k" in channel or "1080p" in channel:
                hd_channels.append(i)
            else:
                sd_channels.append(i)

        return sd_channels, hd_channels

    def write_channels(self, channels, file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for channel in channels:
                print(channel)
                for line in channel:
                    f.write (line)

    def export_channels(self):
        playlist_file = self.playlist_file_path.get()
        

        sd_channels, hd_channels = self.split_channels(playlist_file)

        try:
            os.makedirs("SD")
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        try:
            os.makedirs("HD")
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        self.progress_bar["maximum"] = len(sd_channels) + len(hd_channels)
        self.progress_bar["value"] = 0

        self.log("Exporting SD and HD channels...")
        self.root.update_idletasks()

        self.write_channels(sd_channels, "SD/SD.m3u")
        self.write_channels(sd_channels, "SD/SD.m3u8")
        self.write_channels(hd_channels, "HD/HD.m3u")
        self.write_channels(hd_channels, "HD/HD.m3u8")

        self.log(
            f"{len(sd_channels)} SD channels and {len(hd_channels)} HD channels exported successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = PlaylistSplitterApp(root)
    root.mainloop()

import os
import errno
import customtkinter as tk
from customtkinter import filedialog
import tkinter.messagebox as tkmb


class App(tk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tk.set_appearance_mode("dark")
        self.geometry("500x200")
        self.title("Playlist Splitter by © ncniyazov")
        self.progressbar = tk.CTkProgressBar(self, width=500)
        self.progressbar.set(0)
        self.progressbar.pack()
       
        self.playlist_file_path = tk.StringVar()
        self.chunk_size = tk.IntVar(value=3)
        self.log_text = ""

        self.create_widgets()

    def create_widgets(self):
        tk.CTkLabel(self, text="Select Playlist File:").pack()
        tk.CTkButton(self, text="Browse",
                  command=self.browse_playlist_file).pack()

        tk.CTkLabel(self, text="Chunk Size:").pack()
        tk.CTkEntry(self, textvariable=self.chunk_size).pack()

        tk.CTkButton(self, text="Export",
                  command=self.export_channels).pack()

    def browse_playlist_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("M3U Files", "*.m3u*")])
        if file_path:
            self.playlist_file_path.set(file_path)
      
    def update_progress(self, value):
        self.progress_bar["value"] = value
        self.update_idletasks()

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
                    f.write(line)

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

        #self.log("Exporting SD and HD channels...")
       
        self.update_idletasks()
        self.progressbar.set(50)
        self.progressbar.pack()

        self.write_channels(sd_channels, "SD/SD.m3u")
        self.write_channels(sd_channels, "SD/SD.m3u8")
        self.write_channels(hd_channels, "HD/HD.m3u")
        self.write_channels(hd_channels, "HD/HD.m3u8")

        # self.log(
        #     f"{len(sd_channels)} SD channels and {len(hd_channels)} HD channels exported successfully!")
        tkmb.showinfo(title="Successfully exported!",
                      message=f"{len(sd_channels)} SD channels and {len(hd_channels)} HD channels exported successfully!")
        self.toplevel_window = None
        

if __name__ == "__main__":
    app = App()
    app.mainloop()

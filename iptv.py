import os
import errno


def split_channels(playlist_file):

    playlist = []
    with open(playlist_file, "r", encoding="utf-8") as f:
        for line in f:
            playlist.append(line)
            
    #chunk
    chunk_size = 3

    chunks = [playlist[i:i + chunk_size]
            for i in range(1, len(playlist), chunk_size)]
    result_list = []

    for chunk in chunks:
        result_list.append(chunk)
    #print (result_list)
   
    sd_channels = []
    hd_channels = []


    for i in result_list:
        channel = i[0]
        if "HD" in channel or "4K" in channel or "4k" in channel:
                hd_channels.append(i)
        else:
            sd_channels.append(i)
 
    return sd_channels, hd_channels


def write_channels(channels, file_path):
    """Writes the channels to a file."""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for channel in channels:
            print(channel)
            for line in channel:
                f.write (line)

if __name__ == "__main__":
    playlist_file = "mixed_playlist.m3u8"
    sd_channels, hd_channels = split_channels(playlist_file)

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

    write_channels(sd_channels, "SD/SD.m3u")
    write_channels(hd_channels, "HD/HD.m3u")
    print(f"{len(sd_channels)}  SD channels and {len(hd_channels)} created successfully!")

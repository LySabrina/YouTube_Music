import sys

import requests
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, PytubeError
import os
from ffmpy import FFmpeg, FFRuntimeError

## ask user for the url link
## Check if a directory is created. It should be called: "PyTube_Music"
## From the URL link, get the video title, get the best audio (it will be in mp4 format).
## Before getting the music audio, check if the video title is already installed. If installed, notify user else continue
## convert from mp4 to mp3
## Create a directory full of music.
##

def download_music(link: str) -> None:
    try:
        yt = YouTube(link)
        title = yt.title
        if not check_if_exist(title):
            print("Downloading Music...")
            audio_mp4 = yt.streams.get_audio_only()  # Returns a Stream object
            audio_mp4.download(output_path="./PyTube_Music")
            command = FFmpeg(executable="./ffmpeg", inputs={f'./PyTube_Music/{title}.mp4': None},
                             outputs={f'./PyTube_Music/{title}.mp3': None})
            command.run()

            clean_up_mp4(title+".mp4")

            print("SUCCESSFULLY DOWNLOADED - " + title + ".mp3")

        else:
            print("Music already exist")
    except FFRuntimeError:
        print(f'FFRuntimeError has occurred. Unsuccessfully convert {title} from MP4 to MP3')
        raise
    except VideoUnavailable:
        print(f'Video {title} is unavailable to download')
        raise
    except PytubeError:
        print(f'PyTube could not fetch YouTube Video')
        raise

"""
    Cleans up and remove the MP4 file in the PyTube_Music
    :param mp4: The MP4 file name that needs to be removed
    :type mp4: str
"""
def clean_up_mp4(mp4: str) -> None:
    try:
        file_path = f'./PyTube_Music/{mp4}'
        os.remove(file_path)

    except FileNotFoundError:
        print("COULD NOT FIND FILE")
        raise

"""
    Checks if the PyTube_Music and Temp_Music Directory is created. Creates them if not exist 
    If they do exist, then it checks if the music has already been downloaded
     
    :param title: The title of the YouTube video
    :type title: str
"""


def check_if_exist(title: str) -> bool:
    if not os.path.isdir("./PyTube_Music"):
        os.mkdir("./PyTube_Music")
    current_music = os.listdir("./PyTube_Music")

    for music in current_music:
        if music == title + ".mp3":
            return True
    return False

# Main method
if __name__ == "__main__":
    userInput = input("Enter YouTube URL link to download music from. Type: EXIT to quit program")
    if userInput.lower == 'exit':
        print("GOODBYE")
        sys.exit(0)
    while userInput == "" or userInput[0:23] != "https://www.youtube.com":
        userInput = input("Invalid URL Link. Enter YouTube link again")
        if userInput.lower() == 'exit':
            print("GOODBYE")
            sys.exit(0)
    download_music(userInput)


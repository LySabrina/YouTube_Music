import re
import requests
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, PytubeError
import os
from ffmpy import FFmpeg, FFRuntimeError

"""
    Downloads music based on the URL link given by the user
    :param link: The YouTube URL link the user wants to download the audio into MP3 format
    :type link: str
"""


def download_music(link: str) -> None:
    try:
        yt = YouTube(link)
        title = re.sub(r'[^\w\s]', "", yt.title)  # Removes any punctuation that is in the title
        cover = yt.thumbnail_url

        if not check_if_exist(title):
            print("Downloading Music...")
            audio_mp4 = yt.streams.get_audio_only()  # Returns a Stream object
            audio_mp4.download(output_path="./PyTube_Music")

            print("Downloading Video Thumbnail")
            download_image(cover, title)

            # FFmpeg command line wrapper
            command = FFmpeg(executable="./ffmpeg",
                             inputs={f'./PyTube_Music/{title}.mp4': None,
                                     f'./PyTube_Cover/{title}.jpeg': None
                                     },
                             outputs={
                                 f'./PyTube_Music/{title}.mp3': '-acodec libmp3lame -b:a 256k -c:v copy -map 0:a:0 -map 1:v:0'
                             }
                             )

            command.run()

            clean_up_mp4(title + ".mp4")

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
    Downloads the thumbnail image associated with the YouTube video. It will be used as the cover art for the MP3
    :param img_link: The URL link to the image
    :type: str
    
    :param title: The name of the .jpeg file to be download
    :type title: str
"""


def download_image(img_link: str, title: str) -> None:
    url_req = requests.get(img_link)

    if url_req.status_code == 200:
        print("Successfully fetched Cover Image")
        body_img = url_req.content

        if not os.path.isdir("./PyTube_Cover"):
            os.mkdir("./PyTube_Cover")

        file = open("./PyTube_Cover/" + title + ".jpeg", 'wb')
        file.write(body_img)
        file.close()
    else:
        print("Failed to fetch cover image")


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

    userInput = input("Enter YouTube URL link to download music from. Type: EXIT to quit program\n")
    while userInput.lower() != 'exit':
        if userInput != '' or userInput[0:23] == "https://www.youtube.com":
            download_music(userInput)
            userInput = input("Re-enter YouTube URL link to download music from. Type: EXIT to quit program\n")
        else:
            userInput = input("Invalid URL Link. Enter YouTube link again")

    print("--GOODBYE!")

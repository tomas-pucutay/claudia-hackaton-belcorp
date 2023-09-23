from youtubesearchpython import *
from typing import List, Dict
import yt_dlp
import whisper
import os
import json

BASE_YOUTUBE_PLAYLIST_URL = "https://www.youtube.com/playlist?list="


def get_new_videos(playlist_id: str) -> List:
    """
    Get all the videos from the specified playlist.
    Return an array of dictionaries, every dictionary is a video.
    The information from each video is selected from id, title, link and thumbnail keys
    - playlist_id: str > ID in a youtube playlist
    """
    
    playlist = Playlist(f'{BASE_YOUTUBE_PLAYLIST_URL}{playlist_id}')
    while playlist.hasMoreVideos:
        print('Getting more videos...')
        playlist.getNextVideos()
        print(f'Videos Retrieved: {len(playlist.videos)}')
    
    print("Total number of videos: ", len(playlist.videos))

    videos = [video for video in playlist.videos]

    new_videos = []
    for video in videos:
        video_id = video.get('id')
        video_title = video.get('title')
        video_url = video.get('link')
        video_thumbnail = video.get('thumbnails')[0].get('url')
        new_video = {"id": video_id,
                     "title": video_title,
                     "url": video_url, 
                     "thumbnail": video_thumbnail,
                    }
        new_videos.append(new_video)
    return new_videos

def save_audio(video: Dict):
    """
    It uses yt_dlp to save the audio from the url of an individual video.
    - video: Dict > Video in a dictionary format to extract the url and id
    """
    video_id = video.get('id')
    video_url = video.get('url')
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': f'audio/{video_id}.m4a',
        'noplaylist': True,
        'postprocessors': [{  
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.download(video_url)
    return result    

def get_audio(videos: List) -> Dict:
    """
    From a list of videos, saves the audio from each one.
    And also adds some values that are necessary to match the work already done
    - videos: List > List of videos, each one as a dictionary with relevant keys.
    """
    new_videos = []
    for video in videos:
        try:
            result = save_audio(video)
            video_id = video.get('id')
            video_location = f'audio/{video_id}.m4a'
            
            if(result != 0):
                print("Error downloading audio for video:", video_id)
                continue
            
            new_video = video.copy()
            new_video["audio"] = video_location
            new_video["transcription"] = "NA"
            new_video["transcribed"] = False
            new_video["processed"] = False
            new_videos.append(new_video)
        except Exception as e:
            video_title = video.get('title')
            print("Error downloading audio for episode:", video_title, e)
    return new_videos

def save_new_videos(new_videos: List, existing_videos: List):
    """
    Makes a videos.json file and save the satus of each audio download.
    It prevents to do the same work in the future it its already done.
    - new_videos: List > New videos that will be processed.
    - existing_videos: List > Videos already processed.
    """
    with open('videos.json', 'w') as f:
        f.write(json.dumps(existing_videos + new_videos))


def main():
    """
    Entry point to start downloading youtube videos and saving the audio
    """
    print("Starting")
    # Playlist ID should be changed according to the content needed
    # In this example is the playlist "Lanzamientos" from Belcorp
    playlist_id = "PLxF7HdNkCOLQOAOmQsR3I0I76qklNZucW"
    existing_videos = []
    try:
        with open('videos.json', 'r') as f:
            existing_videos = json.load(f)
    except Exception as e:
        print("Exception when opening file", e)
    videos = get_new_videos(playlist_id)
    existing_videos_id = [video.get('id') for video in existing_videos]
    filtered_videos = [video for video in videos if video.get('id') not in existing_videos_id]
    new_videos = get_audio(filtered_videos)
    save_new_videos(new_videos, existing_videos)

if __name__ == "__main__":
    main()
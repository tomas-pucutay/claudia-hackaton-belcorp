import whisper
import os
from typing import List
import json

def transcribe_audio(path: str):
    """
    Runs whisper model for the audio file sent in the path argument.
    - path: str > Location of the specific m4a audio file.
    """
    model = whisper.load_model("base")
    result = model.transcribe(path)
    return result

def format_transcription(transcription: str):
    """
    Format a transcription as a list of segments with metadata
    - transcription: str > Text of transcription from a video
    """
    formatted_segments = []
    for segment in transcription['segments']:
        formatted_segment = {
            'start': segment['start'],
            'end': segment['end'],
            'text': segment['text']}
        formatted_segments.append(formatted_segment)
    return formatted_segments

def save_transcription(transcription: List, filename: str, directory: str = "transcriptions"):
    """
    Save the formatted transcription in directory
    - transcription: List > List of segments from transcription
    - filename: str > Name for the output file.
    - directory: str > Place where it will be located.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(f'{directory}/{filename}', 'w') as f:
        f.write(json.dumps(transcription))
    print("Transcription saved")

def save_updated_videos(videos: List, filename: str = "videos.json"):
    """
    Update the keys from the videos.json related to transcript flag
    - videos: List > List of videos transcripted.
    - filename: str > Name for output in json file.
    """
    with open(filename, 'w') as f:
        f.write(json.dumps(videos))
    print("Updated videos saved")

def main():
    """
    Entry point to transcribe the audio downloaded in the previous step
    It will get the location of the audio files from videos.json file
    """
    print("Starting")
    directory = "transcriptions"
    with open('videos.json', 'r') as f:
        videos = json.load(f)
        if(len(videos) == 0):
            print("No videos to transcribe")
            pass
        for video in videos:
            if video['processed'] == True or video['transcribed'] == True:
                print("Video already transcribed or processed")
                continue
            audio_path = video['audio']
            filename = video['title'].replace(" ", "_").replace("/","_") + ".json"
            transcription = transcribe_audio(audio_path)
            formatted_transcription = format_transcription(transcription)
            save_transcription(formatted_transcription, filename, directory)
            video['transcription'] = f'{directory}/{filename}'
            video['transcribed'] = True
            save_updated_videos(videos)

if __name__ == "__main__":
    main()
import time
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from dotenv import load_dotenv
from typing import List
import os

_ = load_dotenv()
OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')

def to_chunks(name, link, transcription_path, chunk_length=1000):
    metadatas = []
    try:
        with open(transcription_path, 'r') as f:
            transcript = json.loads(f.read())
        transcript_text_list = [t['text'] for t in transcript]
        transcript_text = ' '.join(transcript_text_list)
        text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
        )
        chunks = text_splitter.split_text(transcript_text)
        for chunk in chunks:
            metadata = {'name': name, 'link': link}
            metadatas.append(metadata)
        return chunks, metadatas
    except Exception as e:
        print("Error reading transcription", e)
        return [], []

def save_embedings(persist_directory: str = "db", chunks: list = None, metadatas: list = None):
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_texts(chunks, embeddings, metadatas=metadatas, persist_directory=persist_directory)

def save_updated_videos(videos: List, filename: str = "videos.json"):
    with open(filename, 'w') as f:
        f.write(json.dumps(videos))

def main():
    print("Starting")
    persist_directory = "../db"
    with open('videos.json', 'r') as f:
        videos = json.load(f)
        if(len(videos) == 0):
            print("No videos to process")
            return
        for video in videos:
            if video['processed'] == True or video['transcribed'] == False:
                print("Episode already processed or not transcribed yet")
                continue
            transcription_path = video['transcription']
            url = video['url']
            title = video['title']
            print("Processing", title)
            chunks, metadatas = to_chunks(title, url, transcription_path)
            if(len(chunks) == 0 or len(metadatas) == 0):
                print("No chunks to process due to an exception for", title)
                continue
            try:
                save_embedings(persist_directory, chunks, metadatas)
                video['processed'] = True
                save_updated_videos(videos)
                time.sleep(1)
            except Exception as e:
                print("Error saving embedings", e)
                continue

if __name__ == "__main__":
    main()
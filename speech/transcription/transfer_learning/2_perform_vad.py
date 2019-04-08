import os
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from utils import vad
from utils import misc
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

def main():
"""Performs Voice Activity detection and chunks the audio files into chunks which are stored in a specified folder  """
    chunk_folder_path = "/home/absin/Documents/dev/sentenceSimilarity/speech/transcription/transfer_learning/calls/chunks/"
    source_folder_path = "/home/absin/Documents/dev/sentenceSimilarity/speech/transcription/transfer_learning/calls/"
    call_paths = os.listdir(source_folder_path)
    print("going to chunk "+str(len(call_paths)) + " for vad")
    with ThreadPoolExecutor(max_workers=10) as executor:
        for call_path in call_paths:
            vad.perform_vad(call_path, chunk_folder_path, 2.5, 10.0)

if __name__ == '__main__':
    main()

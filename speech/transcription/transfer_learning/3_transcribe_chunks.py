import sys
from os import path
sys.path.append( path.dirname(path.dirname( path.dirname( path.abspath(__file__) ) ) ) )
from utils import vad
from utils import misc
from utils import objects
from utils import redis_api
import contextlib
import shutil
import wave
from transcription import google_transcribe
from analysis import main as ana
import pdb
import jsonpickle
from emotion import emotion_api
import requests
import json
import time
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import re
import psycopg2
import os
import redis

def clean_text(text):
    p = re.compile("[^a-z\\s']")
    return p.sub(' ', text)

def transcribe_and_db(chunk_folder_path, chunk_path, speaker, language, model, phrases, conn, cur):
    check_if_already_done_sql = "select * from chunks where file_name = '"+chunk_path.split('/')[-1]+"'"
    cur.execute(check_if_already_done_sql)
    rows = cur.fetchall()
    convs = []
    if len(rows)>0:
        print('Skipping: '+chunk_path+', already done')
        return
    while redis_api.check_entries(pool) > 100:
        time.sleep(61)
        print("Sleeping for 61 seconds while processing: "+chunk_path)
    redis_api.add_entry(pool)
    snippet = objects.Snippet(chunk_folder_path + chunk_path, 0, 0)
    try:
        convs = google_transcribe.transcribe_streaming(snippet, speaker, language, model, phrases)
    except Exception as e:
        print(e)
    if len(convs) > 0:
        transcription = convs[0].text.replace("'","''")
    else:
        transcription = ''
    try:
        file_size = os.stat(chunk_folder_path + chunk_path).st_size
        sql = "INSERT INTO public.chunks (file_name, abs_path, transcription, url, created_at, updated_at, file_size, is_verified) "+"VALUES('"+chunk_path.split('/')[-1]+"', '"+chunk_folder_path+chunk_path+"', '"+transcription+"', NULL, now(), now(), "+str(file_size)+", false);"
        cur.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)

def main():
    """ Performs transcription of all the chunks and stores the results in a database.
    For every chunk entry in the db is checked, if found the transcription is also stored in the database"""
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    chunk_folder_path = "/home/absin/Documents/dev/sentenceSimilarity/speech/transcription/transfer_learning/chunks/"
    chunk_paths = os.listdir(chunk_folder_path)
    phrases=[]
    try:
        ana.append_phrases(phrases, "17918726")
    except Exception as e:
        print('Fetching speech context failed because: ')
        print(e)
    print("The hints for the transcription will be as follows: ")
    print(phrases)
    host = input("Enter DB host: ")
    password = input("Enter DB password: ")
    start = time.time()
    try:
        conn = psycopg2.connect("dbname='sales' user='postgres' host='"+host+"' password='"+password+"'")
    except:
        print('Establishing connection with db failed')
    print("Connection established successsfully after: "+str(time.time()-start))
    cur = conn.cursor()
    transcription_futures = []
    # Check the install.sh for the table schema
    with ThreadPoolExecutor(max_workers=50) as executor:
        for chunk_path in chunk_paths:
            try:
                transcription_futures.append(executor.submit(transcribe_and_db,chunk_folder_path, chunk_path, "Agent", "en-US", True, phrases, conn, cur))
            except:
                print('Failed for snippet: '+chunk_path)
    #for transcription_future in transcription_futures:


if __name__ == '__main__':
    main()

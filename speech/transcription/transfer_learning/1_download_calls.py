import psycopg2
import time
import requests
import os
import sys
from os import path
sys.path.append( path.dirname(( path.dirname( path.dirname( path.abspath(__file__) ) ) )))
from utils import misc
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

"""Fetches all the calls made by ECC using sql connects with the system, takes the SQL host and password from the command line:"""
def main():
    downloaded_task_count = 0
    folder = "/home/absin/Documents/dev/sentenceSimilarity/speech/transcription/transfer_learning/calls/"
    if os.path.exists(folder):
        shutils.rmtree(folder)
    host = input("Enter host: ")
    password = input("Enter password: ")
    start = time.time()
    sql = 'select * from task where actor in (select org_user.userid from org_user where org_user.organizationid = 67) limit 10'
    try:
        conn = psycopg2.connect("dbname='sales' user='postgres' host='"+host+"' password='"+password+"'")
    except:
        print('Establishing connection with db failed')
    print("Connection established successsfully after: "+str(time.time()-start))
    cur = conn.cursor()
    try:
        cur.execute(sql)
    except:
        print("Query fetch failed")
    rows = cur.fetchall()
    print("Fetched "+str(len(rows))+" after: "+str(time.time()-start))
    with ThreadPoolExecutor(max_workers=50) as executor:
        for row in rows:
            file_name = str(row[0])+'.wav'
            url = 'https://storage.googleapis.com/istar-static/' + file_name
            try:
                executor.submit(misc.download_file, url, folder)
                downloaded_task_count += 1
            except:
                print('Downloading failed for: '+file_name)

if __name__ == '__main__':
    main()

import psycopg2
import time
import requests
import os

def download_file(url, folder):
    local_filename = url.split('/')[-1]
    if not os.path.exists(folder):
    	os.makedirs(folder)
    print('Downloading file ' + local_filename + ' ... to '+folder)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(folder + local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush()
    return folder + local_filename

"""Fetches all the calls made by ECC using sql connects with the system, takes the SQL host and password from the command line:"""
def main():
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
    for row in rows:
        file_name = str(row[0])+'.wav'
        url = 'https://storage.googleapis.com/istar-static/' + file_name
        try:
            download_file(url, folder)
        except:
            print('Downloading failed for: '+file_name)

if __name__ == '__main__':
    main()

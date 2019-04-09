import psycopg2
import time

def fetch_chunks(page, host, password):
    start = time.time()
    try:
        conn = psycopg2.connect("dbname='sales' user='postgres' host='"+host+"' password='"+password+"'")
    except:
        print('Establishing connection with db failed')
    print("Connection established successsfully after: "+str(time.time()-start))
    cur = conn.cursor()
    sql = 'select * from chunks order by id desc limit 100 offset ' + str(int(page)*100)
    try:
        cur.execute(sql)
    except:
        print("Query fetch failed")
    rows = cur.fetchall()
    chunks = []
    for row in rows:
        chunk = {"id":row[0], "url": "/audio/"+row[1], "transcription": row[3], "is_verified": row[8]}
        chunks.append(chunk)
    return chunks

def fetch_chunk(chunk_id, host, password):
    start = time.time()
    try:
        conn = psycopg2.connect("dbname='sales' user='postgres' host='"+host+"' password='"+password+"'")
    except:
        print('Establishing connection with db failed')
    print("Connection established successsfully after: "+str(time.time()-start))
    cur = conn.cursor()
    sql = 'select * from chunks where id =  ' + chunk_id
    try:
        cur.execute(sql)
    except:
        print("Query fetch failed")
    rows = cur.fetchall()
    chunks = []
    for row in rows:
        chunk = {"id":row[0], "url": "/audio/"+row[1], "transcription": row[3], "is_verified": row[8]}
        chunks.append(chunk)
    return chunks

def mark_chunk_as_verified(chunk_id, host, password, is_verified):
    start = time.time()
    try:
        conn = psycopg2.connect("dbname='sales' user='postgres' host='"+host+"' password='"+password+"'")
    except:
        print('Establishing connection with db failed')
    print("Connection established successsfully after: "+str(time.time()-start))
    cur = conn.cursor()
    sql = 'update chunks set is_verified = true, updated_at = now() where id = '+str(chunk_id)
    if not is_verified:
        sql = 'update chunks set is_verified = false, updated_at = now() where id = '+str(chunk_id)
    try:
        cur.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
    return fetch_chunk(chunk_id, host, password)

def update_chunk_transcription(chunk_id, host, password, transcript):
    start = time.time()
    try:
        conn = psycopg2.connect("dbname='sales' user='postgres' host='"+host+"' password='"+password+"'")
    except:
        print('Establishing connection with db failed')
    print("Connection established successsfully after: "+str(time.time()-start))
    cur = conn.cursor()
    sql = "update chunks set transcription = '"+transcript+"', updated_at = now() where id = "+str(chunk_id)
    try:
        cur.execute(sql)
        conn.commit()
    except:
        print("Query fetch failed")
    return fetch_chunk(chunk_id, host, password)

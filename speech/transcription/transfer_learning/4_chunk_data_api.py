import psycopg2

def fetch_chunks(page, host, password):
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

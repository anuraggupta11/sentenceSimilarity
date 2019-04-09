import csv
import random

def write_to_csv(csv_path, lines):
    with open(csv_path, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(lines)

def main():
    dev_folder_path = '/home/absin/Documents/dev/sentenceSimilarity/speech/transcription/transfer_learning/final/dev/'
    test_folder_path = '/home/absin/Documents/dev/sentenceSimilarity/speech/transcription/transfer_learning/final/test/'
    train_folder_path = '/home/absin/Documents/dev/sentenceSimilarity/speech/transcription/transfer_learning/final/train/'
    dev_csv_path = '/home/absin/Documents/dev/sentenceSimilarity/speech/transcription/transfer_learning/final/dev.csv'
    test_csv_path = '/home/absin/Documents/dev/sentenceSimilarity/speech/transcription/transfer_learning/final/test.csv'
    train_csv_path = '/home/absin/Documents/dev/sentenceSimilarity/speech/transcription/transfer_learning/final/train.csv'
    header_row = ["wav_filename","wav_filesize","transcript"]
    dev_rows = [header_row]
    test_rows = [header_row]
    train_rows = [header_row]
    host = input("Enter host: ")
    password = input("Enter password: ")
    start = time.time()
    sql  = 'select * from chunks'
    try:
        conn = psycopg2.connect("dbname='sales' user='postgres' host='"+host+"' password='"+password+"'")
        print("Database Connection established successsfully after: "+str(time.time()-start))
    except:
        print('Establishing connection with db failed')
        raise
    cur = conn.cursor()
    try:
        cur.execute(sql)
    except:
        print("Query fetch failed")
        raise
    rows = cur.fetchall()
    print("Fetched "+str(len(rows))+" chunks from database after: "+str(time.time()-start))
    data_rows = []
    for row in rows:
        # Balance between transcription length and audio length, should be more than .003
        balance = row[3]/row[7]
        if balance > 0.003:
            print("Skipping chunk file: " + row[2] + " has unbalanced character " + str(balance) + " perform audit")
            continue
        if not row[8]:
            print("Skipping chunk file: " + row[2] + " has not been marked as verified")
            continue
        data_rows.append([row[2], row[7], row[3]])
    print('Number of chunks on which training, dev, test split will be done: '+str(len(data_rows)))
    for data_row in data_rows:
        ran = random.random() * 100
        if ran < 70:
            # 70% for train
            train_rows.append(data_row)
            misc.copy_files(data_row[0], train_folder_path)
        elif ran >= 70 and ran < 90:
            # 20% for dev
            dev_rows.append(data_row)
            misc.copy_files(data_row[0], dev_folder_path)
        else:
            # 10% for train
            test_rows.append(data_row)
            misc.copy_files(data_row[0], test_folder_path)
    write_to_csv(dev_csv_path, dev_rows)
    write_to_csv(test_csv_path, test_rows)
    write_to_csv(train_csv_path, train_rows)
    print('Done, number of train files: '+str(len(train_rows)))
    print('Done, number of test files: '+str(len(test_rows)))
    print('Done, number of dev files: '+str(len(dev_rows)))

if __name__ == '__main__':
    main()

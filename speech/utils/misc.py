from scipy.io import wavfile
from pathlib import Path
import shutil
import requests
import os 

def split_stereo(file_path, destination_folder = 'NA'):
	fs, data = wavfile.read(file_path)            # reading the file
	file_name = Path(file_path).resolve().stem
	if destination_folder == 'NA':
		# make the destination folder as the same folder of the file
		destination_folder = os.path.dirname(file_path) + '/' + file_name + '/'
		if os.path.isdir(destination_folder):
			shutil.rmtree(destination_folder)
		os.makedirs(destination_folder)
	split_file_1 = destination_folder + file_name + '_1.wav'
	split_file_2 = destination_folder + file_name + '_2.wav'
	wavfile.write(split_file_1, fs, data[:, 0])   # saving first column which corresponds to channel 1
	wavfile.write(split_file_2, fs, data[:, 1])   # saving second column which corresponds to channel 2
	return [split_file_1, split_file_2]

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
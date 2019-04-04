
python3 -V
# should show >3.5.2
sudo apt-get install python3-dev
sudo apt-get install build-essential
sudo apt-get install virtualenv
virtualenv -p python3.6 venv
source venv/bin/activate
pip3 install Flask tensorflow tensorflow-hub keras numpy librosa webrtcvad requests jsonpickle pandas
pip3 install --upgrade google-cloud-speech
# For the google speech to text api to work
echo $GOOGLE_APPLICATION_CREDENTIALS
# should show the path of the json file
# For running notebooks install below:
pip3 install ipykernel
ipython kernel install --user --name=venv

# For running web either
python web.py
# Or you can also use gunicorn server
pip3 install gunicorn
gunicorn --workers 5 -b 0.0.0.0:5010 wsgi:app

# test it with:
# http://0.0.0.0:5010/transcibe_emotion?language=en-IN&model=False&task_id=17913210
# http://0.0.0.0:5010/transcibe_emotion?language=en-IN&model=False&task_id=17913211
# http://0.0.0.0:5010/emotion?task_id=17908876
# http://0.0.0.0:5010/emotion?task_id=17912106
# http://35.244.16.25:5010/transcibe?task_id=17906563&language=en-IN&model=False

# To smoothen deployment even more, create a service

vi /etc/systemd/system/sentenceSimilarity.service


[Unit]
Description=Gunicorn instance to serve our python project
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/root/sentenceSimilarity
Environment="PATH=/root/sentenceSimilarity/venv/bin"
Environment="GOOGLE_APPLICATION_CREDENTIALS=/root/nlptestproject-34c2ad35c9b2.json"
ExecStart=/root/sentenceSimilarity/venv/bin/gunicorn --workers 8 --bind 0.0.0.0:5010 --timeout 1000 --error-logfile /root/sentenceSimilarity/err.out wsgi:app --capture-output --enable-stdio-inheritance

[Install]
WantedBy=multi-user.target



systemctl start sentenceSimilarity.Service
systemctl status sentenceSimilarity.Service
systemctl stop sentenceSimilarity.Service

# Some ffmpeg magic
ffmpeg -i 17916689_002.wav -i 17916689_002.wav -filter_complex '[0:0][1:0]concat=n=2:v=0:a=1[out]' -map '[out]' output.wav

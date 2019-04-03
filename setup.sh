
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

# To smoothen deployment even more, create a service

vi /etc/systemd/system/sentenceSimilarity.service


[Unit]
Description=Gunicorn instance to serve myproject
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/root/deployment/sentenceSimilarity
Environment="PATH=/root/deployment/venv/bin"
ExecStart=/root/deployment/venv/bin/gunicorn --workers 5 -b 0.0.0.0:5010 wsgi:app

[Install]
WantedBy=multi-user.target


systemctl start sentenceSimilarity.Service
systemctl status sentenceSimilarity.Service
systemctl stop sentenceSimilarity.Service

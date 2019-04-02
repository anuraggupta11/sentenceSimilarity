$ python -m venv projectname
$ source projectname/bin/activate
(venv) $ pip install ipykernel
(venv) $ ipython kernel install --user --name=projectname

virtualenv -p python3.6 venv
pip3 install librosa
pip3 install numpy
pip3 install matplotlib
pip3 install tensorflow
pip3 install keras
pip3 install sklearn
pip3 install pandas


pip3 install ipykernel
ipython kernel install --user --name=venv

test it with http://0.0.0.0:5010/transcibe_emotion?language=en-IN&model=False&task_id=17913210
and 17913211


Learnings from text sentenceSimilarity deployed @flask:


/root/deployment/venv/bin/python3.6 /root/deployment/venv/bin/gunicorn --workers 10 -b 0.0.0.0:5010 wsgi:app

vi /etc/systemd/system/sentenceSimilarity.service

[Unit]
Description=Gunicorn instance to serve myproject
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/root/deployment/sentenceSimilarity
Environment="PATH=/root/deployment/venv/bin"
ExecStart=/root/deployment/venv/bin/gunicorn --workers 10 -b 0.0.0.0:5010 wsgi:app

[Install]
WantedBy=multi-user.target

systemctl start sentenceSimilarity.Service
systemctl status sentenceSimilarity.servic
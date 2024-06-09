#!/bin/bash

python3 restore.py

python3 manage.py makemigrations
python3 manage.py migrate
python3 createsuperuser.py

nohup python3 tasks.py &
nohup python3 backup.py -s 15 &

exec ./start_server.sh
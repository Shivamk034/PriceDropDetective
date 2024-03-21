# export DISPLAY=:99
# Xvfb :99 -screen 0 1024x768x24 &

python3 manage.py makemigrations
python3 manage.py migrate
python3 createsuperuser.py

nohup python3 tasks.py &
python3 manage.py runserver 0.0.0.0:8000
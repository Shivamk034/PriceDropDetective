python3 manage.py makemigrations
python3 manage.py migrate

nohup python3 tasks.py &
python3 manage.py runserver 0.0.0.0:8000
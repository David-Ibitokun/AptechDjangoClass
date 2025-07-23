@echo off
cd /d C:\Users\ibito\Documents\Django_Class
call venv\Scripts\activate
python manage.py makemigrations
python manage.py migrate
python manage.py populate_categories
python manage.py createsuperuser
pause

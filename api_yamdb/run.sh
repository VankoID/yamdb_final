python manage.py migrate
python manage.py collectstatic --no-input
gunicorn api_yamdb.wsgi:application --bind 0:8000

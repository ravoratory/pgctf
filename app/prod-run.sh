python manage.py collectstatic --noinput
uwsgi --ini /code/app/uwsgi.ini -w app.wsgi

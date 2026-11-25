web: python manage.py migrate && python manage.py loaddata initial_data.json && python manage.py collectstatic --noinput && gunicorn config.wsgi:application

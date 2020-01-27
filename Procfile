web: gunicorn hwahae_api.wsgi --log-file -
migrate: python manage.py migrate --settings=hwahae_api.settings.production
seed: python manage.py loaddata db.json
web: gunicorn hwahae_api.wsgi --log-file -
migrate: python manage.py migrate --settings=hwahae_api.settings.production
seed: python manage.py seed_ingredients hwahae_api/ingredients/fixtures/ingredient-data.json && python manage.py seed_products hwahae_api/products/fixtures/item-data.json
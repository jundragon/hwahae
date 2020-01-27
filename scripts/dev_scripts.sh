#!/bin/sh

# seed data test
# cd .. && python manage.py test hwahae_api.functional_tests

# products unit test
# cd .. && python manage.py test hwahae_api.products

# ingredients unit test
# cd .. && python manage.py test hwahae_api.ingredients

# run
cd .. 
python manage.py makemigrations --settings=hwahae_api.settings.local
python manage.py migrate --settings=hwahae_api.settings.local
python manage.py seed_ingredients hwahae_api/ingredients/fixtures/ingredient-data.json --settings=hwahae_api.settings.local
python manage.py seed_products hwahae_api/products/fixtures/item-data.json --settings=hwahae_api.settings.local
python manage.py runserver --settings=hwahae_api.settings.local
#!/bin/sh

# seed data test
cd .. && python manage.py test hwahae_api.functional_tests

# products unit test
# cd .. && python manage.py test hwahae_api.products

# ingredients unit test
# cd .. && python manage.py test hwahae_api.ingredients
import pytest
from django.test import Client  

# from django.conf import settings
# settings.DATABASES['default'] = {
#     'ENGINE': 'django.db.backends.sqlite3',
#     'NAME': ':memory:',
# }

@pytest.fixture(scope='session')
def django_test_client():
    
    """
    Django test client fixture
    """
    client = Client()
    return client
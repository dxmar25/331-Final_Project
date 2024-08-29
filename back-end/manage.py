#!/usr/bin/env python
from django.core.management import execute_from_command_line
"""Django's command-line utility for administrative tasks."""
import os
import sys

"""
A command-line utility that lets you interact with this Django project in various ways. 
You can read all the details about manage.py in django-admin and manage.py. - https://docs.djangoproject.com/en/5.0/ref/django-admin/
"""
def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revs_backend.settings')
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

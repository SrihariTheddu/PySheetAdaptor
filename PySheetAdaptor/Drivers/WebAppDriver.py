#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.urls import path
from django.shortcuts import render
from pathlib import Path
from django.core.wsgi import get_wsgi_application

DEBUG = True

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
]
ROOT_URLCONF = 'webapp'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [r"Files"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
SECRET_KEY ="gwiufgeiu984864ne#$%^uhjhdjhfgrgujrh"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': Path(__file__).resolve().parent.parent / 'db.sqlite3',
    }
}
#=========================================================================================================================================
## urls and views are here.............
app_name = "myapp"

def home(request):
    return render(request,"home.html")
urlpatterns = [
  path("",home,name="home")
]
#==================================================================================================================
os.environ.setdefault('DJANGO_SETTINGS_MODULE' , '')
application = get_wsgi_application()
WSGI_APPLICATION = 'webapp.application'

def run():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE' , '')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "To run this application you need to install django... "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(["webapp","runserver"])
#=================================================================================================
if __name__ == '__main__':
    run()





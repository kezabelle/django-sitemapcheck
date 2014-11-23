# -*- coding: utf-8 -*-
import logging
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = (
    'django.contrib.sites',
    'django.contrib.sitemaps',
)

ROOT_URLCONF = 'test_urls'

# Use a fast hasher to speed up tests.
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

SITE_ID = 1

TEMPLATE_CONTEXT_PROCESSORS = ()

HERE_DIR = os.path.abspath(os.path.dirname(__file__))

TEMPLATE_DIRS = ()

SILENCED_SYSTEM_CHECKS = [
    "1_7.W001",
]

USE_TZ = True

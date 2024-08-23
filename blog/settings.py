"""
Django settings for blog project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-c#f%01dcc$d=tn#2suww3v!32dyuj%ovf%(*&2o7%*^%^a(^pe'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #custom apps
    'blogs.apps.BlogsConfig',
    'comments.apps.CommentsConfig',
    'core.apps.CoreConfig',
    'authentication.apps.AuthenticationConfig',
    'rest_framework',
    'drf_yasg',
    'django_select2',
]

'''
You can customize DRF’s behavior through settings in your settings.py file. 
For example, you can set the default pagination, authentication, and permissions.
'''

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,

    #Throttling: Implement throttling to prevent abuse of your API.

    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '100/day',
        'anon': '10/hour',
    },
}



'''
DEFAULT_AUTHENTICATION_CLASSES: Defines the authentication methods to be used. 
Here, we're using both session and token authentication.

DEFAULT_PERMISSION_CLASSES: Defines the default permissions. 
IsAuthenticatedOrReadOnly means that authenticated users can perform write operations, while others can only read.

DEFAULT_PAGINATION_CLASS and PAGE_SIZE: Sets the pagination class and the number of items per page.
'''


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    
    #'default': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': BASE_DIR / 'db.sqlite3',
    #}

    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'blogdb',  # Make sure this matches the database name you created
        'USER': 'admin',  # Make sure this matches the username you created
        'PASSWORD': 'admin',  # Replace with the password you set for the 'admin' user
        'HOST': 'localhost',
        'PORT': '5432',
    }

}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


# URL to use when referring to static files located in STATICFILES_DIRS
STATIC_URL = '/static/'

# The absolute path to the directory where collectstatic will collect static files for deployment
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

'''
STATIC_URL:

This defines the base URL for your static files. When you use {% static 'path/to/file' %}, Django will generate URLs starting with /static/. This URL is used to access your static files in templates and views.
STATIC_ROOT:

This is the directory where Django will collect all the static files when you run the collectstatic command. This is particularly useful in a production environment where you serve static files from a single directory.
For development, you usually don’t need to worry about STATIC_ROOT, but in production, you’ll point your web server to serve files from this directory.
STATICFILES_DIRS:

This is a list of directories where Django will look for additional static files apart from the ones in your apps’ static folders. This allows you to store global static files (like global CSS, JavaScript, or images) in a separate directory within your project.
In the example above, the directory static is assumed to be in the root of your project (BASE_DIR), and it will contain all your custom static files.
'''

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#LOGIN_REDIRECT_URL = 'post_list'
LOGOUT_REDIRECT_URL = 'login'


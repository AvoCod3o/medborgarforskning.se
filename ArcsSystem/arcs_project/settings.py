"""
Django settings for arcs_project project.

Generated by 'django-admin startproject' using Django 2.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bre=h5g+29%aw6&cpwbn9b75&ei&-=h_*c3778rcd9j%avnp-g' # TODO extract to environment variable

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True # TODO extract to environment variable

### use domain name not IP address for security
ALLOWED_HOSTS = ['localhost','127.0.0.1', '0.0.0.0','dev.medborgarforskning.se', 'arcstest.brierjon.com']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps', # enables django to generate sitemap
    'blog', # enables the blog app of ArcsCore
    'products', # enables the products app of ArcsCore
    'projects', # enables the projects app of ArcsCore
    'users', # initializes CustomUser and users app a.k.a. "People app" of ArcsCore
    'django_summernote', # Installing summernote (CK)
    
### Wagtail app requirement start #
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',

    'modelcluster',
    'taggit',
    'wagtail.contrib.modeladmin', # for wagtail menus
    'wagtailmenus', # initialize wagtail menus
### Wagtail app requirement end #
### Wagtail forms install #
    #'wagtail.wagtailforms',
### Wagtail forms install end #
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ### Wagtail app requirement start #
    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    ### Wagtail app requirement end #
]

ROOT_URLCONF = 'arcs_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz', # adds TIME_ZONE variable to RequestContext
                'wagtailmenus.context_processors.wagtailmenus',
            ],
        },
    },
]

WSGI_APPLICATION = 'arcs_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# TODO replace sqlite3 with postgresql
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'myproject',
#        'USER': 'myprojectuser',
#        'PASSWORD': 'password',
#        'HOST': 'localhost',
#        'PORT': '',
#    }
#}
DATABASES = { # TODO switch to postgres
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/arcs_collected_static/static/' # set the location where collectstatic command will place the collected files for serving
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] # sets where collectstatic command will look for static files to include in collection


# Media files (Users uploaded)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Set Wagtail Site Name
WAGTAIL_SITE_NAME = 'Pages and Blog of ARCS'

# Enable our CustomUser abstract user for futurproofing and custom auth uses
AUTH_USER_MODEL = 'users.CustomUser'

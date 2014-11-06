"""
Django settings for asa project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'oxbn3@%nzte&qy-l-#a^q1lis6do*%v_8x5r*!!o4u+$%19wim'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []

# added by danny
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]


# ==============================
# Django allauth settings
# ==============================
TEMPLATE_CONTEXT_PROCESSORS = (
    # required by allauth template tags
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    # allauth specific context processors
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by email
    "allauth.account.auth_backends.AuthenticationBackend",
)
SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = "none"

# auth and allauth settings
LOGIN_REDIRECT_URL = '/'
# === END Djanog allauth settings


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'twitch',
    'info',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'asa',
    'broadcast',
    'profile',
    #'captcha',
    'hot',
    'rest_framework',
    'twitter',
    'sentimentAnalysis',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'asa.urls'

#WSGI_APPLICATION = 'asa.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#WHOOSH_INDEX=[os.path.join(BASE_DIR, 'whoosh/')]

#HAYSTACK_CONNECTIONS= {
#	'default':{
#		'ENGINE' : 'haystack.backends.whoosh_backend.WhooshEngine',
#		'PATH'   :  WHOOSH_INDEX,
#	},
#}
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# ==========================================================
# Settings from Heroku tutorial - comment out as necessary
#  on your local to get working
# ==========================================================
# Parse database configuration from $DATABASE_URL
#import dj_database_url
#DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Add custom stuff to signup form for django-allauth
ACCOUNT_SIGNUP_FORM_CLASS = 'asa.forms.SignupForm'

# Testing purposes only, True or False manually
# When deploying to Heroku or Pushing to BitBucket SET IT TO False.
CAPTCHA_TEST_MODE = False


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    'PAGINATE_BY': 10,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

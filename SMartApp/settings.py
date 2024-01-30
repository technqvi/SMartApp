
import os
import posixpath
import environ
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS =['127.0.0.1','localhost']

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Application references
# https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-INSTALLED_APPS
INSTALLED_APPS = [
    'app.apps.smAppNameConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'models_logging',
    'crispy_forms',
    'rest_framework',
    'debug_toolbar',
]

# # Log Model
LOGGING_MODELS = (
      'app.PM_Inventory',
      'app.PreventiveMaintenance',
      'app.Project',
      'app.Inventory',
      'app.Incident',
      'app.Incident_Detail',
      'app.Model',
      'app.Customer',
      'app.Product',
      'app.Branch',
      'app.DataCenter',
      'app.Product',
      'app.Customer',
      'app.Company',
)

# Middleware framework
# https://docs.djangoproject.com/en/2.1/topics/http/middleware/
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'models_logging.middleware.LoggingStackMiddleware',  # it merge all changes of object per request
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]


ROOT_URLCONF = 'SMartApp.urls'

# Template configuration
# https://docs.djangoproject.com/en/2.1/topics/templates/
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

WSGI_APPLICATION = 'SMartApp.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DATABASES_NAME'),
        'USER': env('DATABASES_USER'),
        'PASSWORD': env('DATABASES_PASSWORD'),
        'HOST': env('DATABASES_HOST')
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Bangkok'
USE_I18N = True
USE_L10N = True
USE_TZ = True






# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = posixpath.join(*(BASE_DIR.split(os.path.sep) + ['static']))
#STATIC_ROOT = os.path.join(BASE_DIR,'static')

DATA_UPLOAD_MAX_NUMBER_FIELDS=None

SERIAL_NO_DEFAULT='-'
INCIDENT_CODE_CLOSED=4
INCIDENT_CODE_CANCELED=3
INCIDENT_DOC_PATH='incident_docs'
INCIDENT_PREFIX_DOC ='incident_'
INCIDENT_CONTENT_TYPE=['']

DUMMY_CODE='dummy-'
DUMMY_INIT_ID=1

MEDIA_URL = f'/{INCIDENT_DOC_PATH}/'
MEDIA_ROOT = os.path.join(BASE_DIR, INCIDENT_DOC_PATH)
# At hear e is BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

UPLOAD_FILE_TYPES = ['application/pdf','image/jpeg', 'image/png','text/plain',
                  'application/msword','application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                  'application/vnd.ms-excel','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                  'application/vnd.ms-powerpoint','application/vnd.openxmlformats-officedocument.presentationml.presentation']
UPLOAD_FILE_MAX_SIZE_MB = 10
UPLOAD_FILE_UNIT='MB'
#['application/pdf','image/jpeg','application/zip','application/zip','application/gzip','application/vnd.rar','text/csv',#'audio/mpeg',]



from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
        messages.DEBUG: 'alert-default',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
 }

MY_PAGE_NAME='page'
#MY_PAGE_PER= 5
MY_PAGE_PER= 10
MY_YEAR_LOOKUP=2
WARRANTY_EMD_DUMMY_INVENTORY='31/12/2500'



# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'bossanova.net@gmail.com'
# EMAIL_HOST_PASSWORD = 'xxxxxxxxxx'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False

EMAIL_BACKEND = 'django_o365mail.EmailBackend'
O365_MAIL_CLIENT_ID =env('O365_MAIL_CLIENT_ID')
O365_MAIL_CLIENT_SECRET =env('O365_MAIL_CLIENT_SECRET')
O365_MAIL_TENANT_ID =env('O365_MAIL_TENANT_ID')
O365_ACTUALLY_SEND_IN_DEBUG=bool(env('O365_ACTUALLY_SEND_IN_DEBUG'))
O365_MAIL_MAILBOX_KWARGS = {'resource': env('O365_MAIL_MAILBOX_KWARGS')}

EMAIL_ADMIN_FOR_MONTHLY_NOTIFICATION=['pongthorn.sa@yipintsoi.com']

YIP_DOMAIN_NAME=env('YIP_DOMAIN_NAME')
LOG_ERROR_FILE_PATH=env('LOG_ERROR_FILE_PATH')


PM_DOC_FILE_LOCAL_PATH=env('PM_DOC_FILE_LOCAL_PATH')
PM_DOC_FILE_HTTP_PATH= env('PM_DOC_FILE_HTTP_PATH')

PM_PHYSICAL_TEMPLATE_PATH='pdf_pm_html_template'
PM_PHYSICAL_PDF_PATH='pdf_pm_doc'
PM_OVERVIEW_TEMPLATE='pm_overview.html'

PM_OVERVIEW_CSS='pdf_pm_overview.css'
PM_ITEM_CSS='pdf_pm_item.css'
PM_LOGO_IMAGE='logo_mini.png'
PM_DOC_FILE_TYPE=['.pdf']

PURGE_FILE_TYPE=['.zip']
PURGE_DOC_HOUR_PERIOD=1# hour

FIRST_DAY_ALLOWED_TO_FILL_IN_FORM='2019-01-01'

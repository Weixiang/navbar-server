"""
Django settings for navsys project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-c_awwve(hb)_vpjics4=#fykyg&!=r^4=k^hq0l@941lj2qoau"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.1.30', '127.0.0.1', '0.0.0.0']


ENCRYPT = "NONE"
AES_KEY = "9432797835584249"


INSTALLED_APPS = [
    'simpleui',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "navsysMain",
    'rest_framework', 
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "navsys.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "navsys.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

USE_TZ = True  # 启用时区支持
TIME_ZONE = "Asia/Shanghai"  # 设置时区为北京时间

USE_I18N = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SIMPLEUI_ICON = {
    '设备': 'fa-solid fa-microchip',
    '环境': 'fa-solid fa-temperature-three-quarters',
    '物品':'fa-solid fa-box',
    '记录':'fa-solid fa-clipboard-list',
    '仓库':'fa-solid fa-warehouse',
    '阈值': 'fa-solid fa-gauge-high',
}

SIMPLEUI_HOME_TITLE = "NavigationBar Dashboard"

SIMPLEUI_HOME_ICON = 'fa fa-user'

SIMPLEUI_HOME_INFO = False

# SIMPLEUI_LOGO = "/static/icon/apple-touch-icon.png"

# 登录页面
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# MQTT 设置
MQTT_SERVER = "broker.emqx.io"
MQTT_PORT = 8883
MQTT_KEEPALIVE = 60
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_PERFIX = "nav1044"

MQTT_CA_CERTS = "./navsysMain/certificates/broker.emqx.io-ca.crt"
MQTT_CERTFILE = ""
MQTT_KEYFILE = ""

# navsys\navsysMain\certificates\broker.emqx.io-ca.crt

# 企业微信机器人
QYWXBOT_KEY = "506c7b81-7f5f-4f1c-8876-b3adada2af35"

# 日志输出设置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'colored': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s%(levelname)s:%(name)s:%(message)s',
            'log_colors': {
                'DEBUG': 'bold_blue',
                'INFO': 'bold_green',
                'WARNING': 'bold_yellow',
                'ERROR': 'bold_red',
                'CRITICAL': 'bold_purple',
            },
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'colored',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'DB': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'MQTT': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'WEB': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'AES': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )}
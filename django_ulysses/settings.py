"""
Django settings for django_ulysses project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import password
import djcelery
from django.contrib.messages import constants as message_constants

LIGHT = 2
DARK = 4
PRIMARY = 6
SECONDARY = 8
DANGER = 50

MESSAGE_LEVEL = LIGHT
MESSAGE_TAGS = {
    LIGHT: 'light',
    DARK: 'dark',
    PRIMARY: 'primary',
    SECONDARY: 'secondary',
    DANGER: 'danger'
}

djcelery.setup_loader()
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 指定file或image上传目录
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace("\\", "/")

# 使用自定义的模型替代默认User
# AUTH_USER_MODEL = 'users.User'




# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8pqf(8jqsytrh#-%_0tbrxcibvc!p)l_f3mozz7$8h1nty(^wj'

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
    # 创建的应用
    'learning_logs',
    'users',
    'bootstrap4',
    'fullurl',
    'mdeditor',
]
INSTALLED_APPS += ("djcelery", )

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'django_ulysses.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '../../../django_ulysses/learning_logs/templates'),
                 os.path.join(BASE_DIR, '../../../users/templates')],
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
# 设置message存储的区域
# MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

WSGI_APPLICATION = 'django_ulysses.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '../../../django_ulysses/learning_logs/static/'),
]

LOGIN_URL = '/users/login/'

BOOTSTRAP4 = {
    'include_jquery': True,
}
# 邮件设置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER') or "2276777056@qq.com"
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD') or password.EMAIL_HOST_PASSWORD
EMAIL_USE_SSL = True

# Celery设置
# 时区
CELERY_TIMEZONE = 'Asia/Shanghai'
# 中间件
BROKER_URL= 'redis://localhost:6379/0'

CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler' ###


BASE_URL = 'http://127.0.0.1:8000/'

MDEDITOR_CONFIGS = {
    'default': {
        'width': '90% ',  # Custom edit box width
        'heigth': 500,  # Custom edit box height
        'toolbar': ["undo", "redo", "|",
                    "bold", "del", "italic", "quote", "ucwords", "uppercase", "lowercase", "|",
                    "h1", "h2", "h3", "h5", "h6", "|",
                    "list-ul", "list-ol", "hr", "|",
                    "link", "reference-link", "image", "code", "preformatted-text", "code-block", "table", "datetime"
                                                                                                           "emoji",
                    "html-entities", "pagebreak", "goto-line", "|",
                    "help", "info",
                    "||", "preview", "watch", "fullscreen"],  # custom edit box toolbar
        'upload_image_formats': ["jpg", "jpeg", "gif", "png", "bmp", "webp"],  # image upload format type
        'image_floder': 'editor',  # image save the folder name
        'theme': 'default',  # edit box theme, dark / default
        'preview_theme': 'default',  # Preview area theme, dark / default
        'editor_theme': 'default',  # edit area theme, pastel-on-dark / default
        'toolbar_autofixed': True,  # Whether the toolbar capitals
        'search_replace': True,  # Whether to open the search for replacement
        'emoji': True,  # whether to open the expression function
        'tex': True,  # whether to open the tex chart function
        'flow_chart': True,  # whether to open the flow chart function
        'sequence': True  # Whether to open the sequence diagram function
    }

}
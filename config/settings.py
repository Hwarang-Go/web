from pathlib import Path
import os
import json

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# load secret.json
secret_file = os.path.join(BASE_DIR, 'secret.json')
with open(secret_file) as f:
    secrets = json.loads(f.read()) # json 타입의 변수에 secret.json 파일 내용 받아옴

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secrets['SECRET_KEY']
# git 같은 데 올리면 안됨. 그래서 secret.json 파일에 따로 담고 key값으로 불러오도록 함

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
# * 를 리스트 안에 쓰면 모든 주소 들어오는거 가능


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'ex01',
    # 'ex02',
    'board',
    'product',
    'reply',
]

# django에서 쓰는 app들. 위에다 써주면 됨. 여기다 등록하지 않아도 접근자체는 되지만, 후에 migration 할 때 등록되어 있어야하므로 등록할것

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# app들하고 비슷함. 사용자 단이 아니라 중간에서 쓰이는 프로그램들이라고 보면 됨.

ROOT_URLCONF = 'config.urls'
# config/urls.py 파일 뜻함

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates', BASE_DIR/'board/templatetags'],  # templates 폴더 만들고 디렉토리 추가했음
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

WSGI_APPLICATION = 'config.wsgi.application'
# 웹서버와 연결할때 쓰는것

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': secrets['DB_NAME'], # 마리아 db에서 CREATE DATABASE web; 으로 만들어준 그 이름
        'USER': secrets['DB_USER'],
        'PASSWORD': secrets['DB_PASSWORD'],
        'HOST': secrets['DB_HOST'],
        'PORT': secrets['DB_PORT'],
        'OPTIONS': {
            'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"'
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# 개인정보보호를 위해 패스워드 암호화 하는 것. 단방향 암호화(복호화 할 수 있으면 안됨)

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
# 프로젝트 규모가 커지면 app마다 static 폴더를 두고 따로 관리
# 하지만 지금은 규모도 작고 연습용으로 그냥 절대 경로로 두고 하나만 두고 관리
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

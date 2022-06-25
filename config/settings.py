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

    # email 인증 할 때 필요한 거
    'django.contrib.sites', # 여러 사이트 한 서버에서 관리할 때, 여기서는 allauth에서 필요해서 추가함
    'user',
    'allauth',
    'allauth.account',
    'allauth.socialaccount', # 카카오 인증, 네이버 아이디 로그인할 때 쓰이는거

    # allauth kakao login
    'allauth.socialaccount.providers.kakao',
]

# django에서 쓰는 app들. 위에다 써주면 됨. 여기다 등록하지 않아도 접근자체는 되지만, 후에 migration 할 때 등록되어 있어야하므로 등록할것

AUTH_USER_MODEL = 'user.User'

SITE_ID = 1 # 여러 개가 한 서버에서 관리 될 때 구분할 수 있는 아이디, 실습에서는 하나만 쓰는데 그 아이디를 1로 둠

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# 이메일 인증할 때 필요한 거
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = secrets['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = secrets['EMAIL_HOST_PW']  # 앱 비밀 번호
EMAIL_USE_TLS = True  # USE 를 USER라고 해서 계속 smtp auth error 나옴
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[이메일 인증]'

# 회원 가입할 때 인증하는데 뭘로 할거냐
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
# 이렇게 하면 username 없이 email로 한다는것
# 위에 3줄 없을때 signup 페이지에 username 도 있었는데
# 추가하고 새로고침 하니까 email 만 뜸


# 쓸 수 있는 3개 값
# none 인증 안함,
# optional 인증할 수 있는데 로그인은 됨, (default 값) 그래서 터미널에 이메일 내용 나온거
# mandatory 강제적으로 인증해야 로그인되게 함
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

# 보낸 인증 메일 클릭해서 사용자가 접속하면 get 방식으로 들어오면 허용을 시켜줄거냐라는 설정을 True로 한거임
ACCOUNT_CONFIRM_EMAIL_ON_GET = True

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

# 사용자 이미지 올라오는 곳 설정
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # static 은 리스트로 해도 되지만, media 는 하나만 해야함

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

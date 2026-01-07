from pathlib import Path
from datetime import timedelta
from django.conf import settings
from django.conf.global_settings import AUTH_USER_MODEL, MEDIA_ROOT

BASE_DIR = Path ( __file__ ).resolve ().parent.parent

SECRET_KEY = 'django-insecure-!&srf3f*mm%1yqumo6q+$xzbh=rxf79a(=tylp4c2_w06=ei_y'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_app',
    'rest_framework',
    'drf_yasg',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist'
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES' : (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES' : (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME" : timedelta ( minutes=5 ),
    "REFRESH_TOKEN_LIFETIME" : timedelta ( days=1 ),
    "ROTATE_REFRESH_TOKENS" : False,
    "BLACKLIST_AFTER_ROTATION" : False,
    "UPDATE_LAST_LOGIN" : False,

    "ALGORITHM" : "HS256",
    "SIGNING_KEY" : SECRET_KEY,
    "VERIFYING_KEY" : "",
    "AUDIENCE" : None,
    "ISSUER" : None,
    "JSON_ENCODER" : None,
    "JWK_URL" : None,
    "LEEWAY" : 0,

    "AUTH_HEADER_TYPES" : ("Bearer",),
    "AUTH_HEADER_NAME" : "HTTP_AUTHORIZATION",
    "USER_ID_FIELD" : "id",
    "USER_ID_CLAIM" : "user_id",
    "USER_AUTHENTICATION_RULE" : "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "ON_LOGIN_SUCCESS" : "rest_framework_simplejwt.serializers.default_on_login_success",
    "ON_LOGIN_FAILED" : "rest_framework_simplejwt.serializers.default_on_login_failed",

    "AUTH_TOKEN_CLASSES" : ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM" : "token_type",
    "TOKEN_USER_CLASS" : "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM" : "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM" : "refresh_exp",
    "SLIDING_TOKEN_LIFETIME" : timedelta ( minutes=5 ),
    "SLIDING_TOKEN_REFRESH_LIFETIME" : timedelta ( days=1 ),

    "TOKEN_OBTAIN_SERIALIZER" : "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER" : "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER" : "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER" : "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER" : "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER" : "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",

    "CHECK_REVOKE_TOKEN" : False,
    "REVOKE_TOKEN_CLAIM" : "hash_password",
    "CHECK_USER_IS_ACTIVE" : True,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_project.urls'

TEMPLATES = [
    {
        'BACKEND' : 'django.template.backends.django.DjangoTemplates',
        'DIRS' : [],
        'APP_DIRS' : True,
        'OPTIONS' : {
            'context_processors' : [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_project.wsgi.application'

DATABASES = {
    'default' : {
        'ENGINE' : 'django.db.backends.sqlite3',
        'NAME' : BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME' : 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME' : 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME' : 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME' : 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
AUTH_USER_MODEL = 'django_app.User'

EXPIRATION_PHONE = 2
EXPIRATION_EMAIL = 3

MEDIA_ROOT = 'media'
MEDIA_URL = '/media/'
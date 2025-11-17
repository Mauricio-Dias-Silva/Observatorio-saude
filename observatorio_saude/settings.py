# /observatorio_saude/settings.py
# [VERSÃO ATUALIZADA - PRONTA PARA CLOUD RUN + CLOUD SQL]

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-oru+m!fnk=hedmvxyz3me-s7jf7d53u&=mkr4e8-e3-srwkl^z'

# SECURITY WARNING: don't run with debug turned on in production!
# "DECORAÇÃO": DEBUG = False é obrigatório para produção.
DEBUG = False

# "DECORAÇÃO": ['*'] permite que o Cloud Run acesse seu site.
# (Em produção real, você trocaria '*' pela URL do seu serviço).
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    # "DECORAÇÃO": Whitenoise serve os arquivos estáticos (CSS/JS)
    # Deve vir primeiro.
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'analise_saude',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # "DECORAÇÃO": Whitenoise Middleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'observatorio_saude.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'observatorio_saude.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# -----------------------------------------------------------------
# "DECORAÇÃO": CONFIGURAÇÃO DE BANCO DE DADOS PARA CLOUD RUN + CLOUD SQL
# -----------------------------------------------------------------
# Removemos o SQLite e o MySQL. Esta é a configuração correta.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',

        # PREENCHA COM OS DADOS DO SEU CLOUD SQL:
        'NAME': 'pythonjet-db',     # O nome do banco que você criou
        'USER': 'postgres',          # O usuário (geralmente 'postgres')
        
        # !!!!!!!!!!! ATENÇÃO !!!!!!!!!!!
        # COLOQUE A SENHA QUE VOCÊ CRIOU PARA O CLOUD SQL AQUI
        'PASSWORD': 'SUA_SENHA_AQUI', 
        # !!!!!!!!!!! ATENÇÃO !!!!!!!!!!!

        # "DECORAÇÃO": Este é o "caminho mágico" (Unix Socket) para
        # conectar o Cloud Run ao Cloud SQL de forma rápida e segura.
        # Formato: /cloudsql/[PROJECT_ID]:[REGION]:[INSTANCE_NAME]
        'HOST': '/cloudsql/pythonjet:us-east1:pythonjet-db',
        
        'PORT': '5432', # Deixe como 5432
    }
}
# -----------------------------------------------------------------


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# "DECORAÇÃO": Onde o 'collectstatic' vai salvar os arquivos
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# "DECORAÇÃO": Otimização do Whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


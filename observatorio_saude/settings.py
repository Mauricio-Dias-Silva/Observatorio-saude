"""
Django settings for observatorio_saude project.
Configuração Otimizada para Google Cloud Run + Cloud SQL
"""

from pathlib import Path
import os
import dj_database_url  # Biblioteca mágica para conexão de banco

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# SEGURANÇA E AMBIENTE
# ==============================================================================

# Lê a SECRET_KEY do ambiente ou usa uma insegura apenas para testes locais
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-local-dev-key-change-me')

# DEBUG deve ser False na produção. Se a variável não existir, assume False.
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# ALLOWED_HOSTS: Aceita tudo no Cloud Run (o firewall do Google protege)
ALLOWED_HOSTS = ['*']

# Correção para erro de CSRF no Cloud Run (Erro 403 no Login)
# Isso confia na URL do Cloud Run automaticamente
CSRF_TRUSTED_ORIGINS = ['https://*.run.app']

# ==============================================================================
# APLICAÇÕES
# ==============================================================================

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic', # Ajuda a servir estáticos localmente
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Suas Apps
    'analise_saude',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # OBRIGATÓRIO: Serve CSS/JS no Cloud Run
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

# ==============================================================================
# BANCO DE DADOS (A CORREÇÃO DO LOOPING)
# ==============================================================================

# 1. Padrão: Começa com SQLite (para desenvolvimento local funcionar sempre)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 2. Produção: Se existir DATABASE_URL, substitui pelo PostgreSQL
# Isso acontece automaticamente no Cloud Run se você configurar a variável lá.
database_url = os.environ.get('DATABASE_URL')

if database_url:
    DATABASES['default'] = dj_database_url.config(
        default=database_url,
        conn_max_age=600,    # Mantém a conexão viva por 10 min (performance)
        conn_health_checks=True,
        ssl_require=True
    )

# ==============================================================================
# VALIDAÇÃO DE SENHA
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==============================================================================
# INTERNACIONALIZAÇÃO
# ==============================================================================

LANGUAGE_CODE = 'pt-br' # Mudei para PT-BR pois vi que é seu padrão
TIME_ZONE = 'America/Sao_Paulo' # Ajustei fuso
USE_I18N = True
USE_TZ = True

# ==============================================================================
# ARQUIVOS ESTÁTICOS (CSS, JS, IMAGENS)
# ==============================================================================

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Whitenoise: Comprime e faz cache dos arquivos estáticos para ficarem rápidos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ==============================================================================
# CONFIGURAÇÕES ADICIONAIS
# ==============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

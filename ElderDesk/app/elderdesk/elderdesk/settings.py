import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = bool(os.environ.get("DEBUG", default=0))

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

# CSRF_TRUSTED_ORIGINS=['http://127.0.0.1:8000']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', 

    # third party
    # 'crispy_forms',
    # 'crispy_bootstrap5', 
    # 'allauth', 
    # 'allauth.account', 
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.microsoft',

    'django_auth_adfs',
    
    'silk',

    # apps
    'accounts.apps.AccountsConfig',
    'clients.apps.ClientsConfig',
    'tickets.apps.TicketsConfig',
    'organizations.apps.OrganizationsConfig',
    'pages.apps.PagesConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # third party 
    'silk.middleware.SilkyMiddleware',
    'django_auth_adfs.middleware.LoginRequiredMiddleware',
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ROOT_URLCONF = 'elderdesk.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'elderdesk.wsgi.application'


# Database
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    # "allauth.account.auth_backends.AuthenticationBackend", 
    
    'django_auth_adfs.backend.AdfsAuthCodeBackend',
    'django_auth_adfs.backend.AdfsAccessTokenBackend',
)

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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

MEDIA_URL = "/media/" 

MEDIA_ROOT = BASE_DIR / "media" 

STATIC_URL = '/static/'

STATICFILES_DIRS = [BASE_DIR / "static"]

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1

# Microsoft Azure AD configuration
AZURE_CLIENT_ID = os.environ.get('AZURE_CLIENT_ID')
AZURE_TENANT_ID = os.environ.get('AZURE_TENANT_ID')
AZURE_CLIENT_SECRET = os.environ.get('AZURE_CLIENT_SECRET')
AZURE_REDIRECT_URI = os.environ.get('AZURE_REDIRECT_URI')
AZURE_AUTHORITY = os.environ.get('AZURE_AUTHORITY')
AZURE_SCOPES = os.environ.get('AZURE_SCOPES').split()

AUTH_ADFS = {
    'AUDIENCE': [f'api://{AZURE_CLIENT_ID}', AZURE_CLIENT_ID],
    'CLIENT_ID': AZURE_CLIENT_ID,
    'CLIENT_SECRET': AZURE_CLIENT_SECRET,
    "CLAIM_MAPPING": {"first_name": "given_name",
                      "last_name": "family_name",
                      "email": "email"},
    'GROUPS_CLAIM': 'roles',
    'MIRROR_GROUPS': True,
    'USERNAME_CLAIM': 'email',
    'TENANT_ID': AZURE_TENANT_ID,
    'RELYING_PARTY_ID': AZURE_CLIENT_ID,
    'LOGIN_EXEMPT_URLS': [
        '^api',  
        '^$',
        '^admin/',
    ],
}

# ACCOUNT_USERNAME_REQUIRED = False 
# ACCOUNT_AUTHENTICATION_METHOD = "email"
# ACCOUNT_EMAIL_REQUIRED = True 
# ACCOUNT_UNIQUE_EMAIL = True

LOGIN_URL = "django_auth_adfs:login"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = '/'

# django-crispy-forms
# CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5" 
# CRISPY_TEMPLATE_PACK = "bootstrap5"
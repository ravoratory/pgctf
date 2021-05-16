from .settings import *

DEBUG=False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ['DB_PORT'],
    }
}
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    ('css', os.path.join(STATIC_ROOT, 'css')),
    ('img', os.path.join(STATIC_ROOT, 'img')),
    ('js', os.path.join(STATIC_ROOT, 'js')),
    ('html', os.path.join(STATIC_ROOT, 'html')),
)

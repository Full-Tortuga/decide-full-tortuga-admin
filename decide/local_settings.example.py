ALLOWED_HOSTS = ["*"]

# Modules in use, commented modules that you won't use
MODULES = [
    'administration',
    'authentication',
    'base',
    'booth',
    'census',
    'mixnet',
    'postproc',
    'store',
    'visualizer',
    'voting',
]


BASEURL = 'http://localhost:8000'
CORS_ORIGIN_ALLOW_ALL = True

APIS = {
    'administration': BASEURL,
    'authentication': BASEURL,
    'base': BASEURL,
    'booth': BASEURL,
    'census': BASEURL,
    'mixnet': BASEURL,
    'postproc': BASEURL,
    'store': BASEURL,
    'visualizer': BASEURL,
    'voting': BASEURL,
}

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'decide',
        'CLIENT': {
            'host': '127.0.0.1',
        }
    },
    'postgres': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'decide',
        'PASSWORD': 'decide',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# number of bits for the key, all auths should use the same number of bits
KEYBITS = 256

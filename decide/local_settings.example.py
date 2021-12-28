# dev env CORS SETTINGS
BASEURL = 'http://localhost:8000'
FE_BASEURL = 'http://localhost:3000'

ALLOWED_HOSTS = ['*']

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
    BASEURL, FE_BASEURL
)
CSRF_TRUSTED_ORIGINS = [
    BASEURL, FE_BASEURL
]


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
    }
}

# number of bits for the key, all auths should use the same number of bits
KEYBITS = 256

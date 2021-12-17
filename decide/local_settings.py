ALLOWED_HOSTS = ["*"]

CORS_ORIGIN_ALLOW_ALL = True

# Modules in use, commented modules that you won't use
'''MODULES = [
    'authentication',
    'base',
    'booth',
    'census',
    'mixnet',
    'postproc',
    'store',
    'visualizer',
    'voting',
]'''

APIS = {
    'authentication': 'http://localhost:8000',
    'base': 'http://localhost:8000',
    'booth': 'http://localhost:8000',
    'census': 'http://localhost:8000',
    'mixnet': 'http://localhost:8000',
    'postproc': 'http://localhost:8000',
    'store': 'http://localhost:8000',
    'visualizer': 'http://localhost:8000',
    'voting': 'http://localhost:8000',
}

BASEURL = 'http://localhost:8000'

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

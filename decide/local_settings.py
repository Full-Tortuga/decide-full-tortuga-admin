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
    'authentication': 'http://localhost:8011',
    'base': 'http://localhost:8011',
    'booth': 'http://localhost:8011',
    'census': 'http://localhost:8011',
    'mixnet': 'http://localhost:8011',
    'postproc': 'http://localhost:8011',
    'store': 'http://localhost:8011',
    'visualizer': 'http://localhost:8011',
    'voting': 'http://localhost:8011',
}

BASEURL = 'http://localhost:8011'

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'decide',
        'CLIENT': {
           'host': '172.31.0.2',
           'username': 'mongo',
           'password': 'mongo'
        }

    }
}

# number of bits for the key, all auths should use the same number of bits
KEYBITS = 256
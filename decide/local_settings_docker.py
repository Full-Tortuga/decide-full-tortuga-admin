
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType
import os

# dev env CORS SETTINGS
BASEURL = 'http://localhost:8000'
FE_BASEURL = 'http://localhost:3000'

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
        'NAME': 'db',
        'CLIENT': {
            'username': os.environ.get('MONGO_USER'),
            'password': os.environ.get('MONGO_PASSWORD'),
            'host': os.environ.get('MONGO_HOST'),
            'port': int(os.environ.get('MONGO_PORT')),
            'authSource': os.environ.get('MONGO_NAME'),
            'authMechanism': 'SCRAM-SHA-1'
        }
    }
}

# number of bits for the key, all auths should use the same number of bits
KEYBITS = 256

# Baseline configuration.
AUTH_LDAP_SERVER_URI = 'ldap://:389'

AUTH_LDAP_BIND_DN = 'cn=admin,dc=decide,dc=org'
AUTH_LDAP_BIND_PASSWORD = 'decide'
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    'ou=people,dc=decide,dc=org',
    ldap.SCOPE_SUBTREE,
    '(uid=%(user)s)',
)

# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
    'first_name': 'cn',
    'last_name': 'sn',
    'email': 'mail',
}

# Keep ModelBackend around for per-user permissions and maybe a local
# superuser.

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'django_auth_ldap.backend.LDAPBackend',
]

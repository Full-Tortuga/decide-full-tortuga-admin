import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType
import os

DEBUG = True

STATIC_ROOT = '/app/static/'
MEDIA_ROOT = '/app/static/media/'
ALLOWED_HOSTS = ['*']

BASEURL = 'http://localhost'





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

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': os.environ.get('DATABASE_NAME'),
        'CLIENT': {
           'host': os.environ.get('DATABASE_HOST'),
           'username':  os.environ.get('DATABASE_USER'),
           'password': os.environ.get('DATABASE_PASSWORD'),
	       'SSL': 'true'
        }

    }
}

# number of bits for the key, all auths should use the same number of bits
KEYBITS = 256

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
APIS = {
    'administration': 'http://10.5.0.1:8000',
    'authentication': 'http://10.5.0.1:8000',
    'base': 'http://10.5.0.1:8000',
    'booth': 'http://10.5.0.1:8000',
    'census': 'http://10.5.0.1:8000',
    'mixnet': 'http://10.5.0.1:8000',
    'postproc': 'http://10.5.0.1:8000',
    'store': 'http://10.5.0.1:8000',
    'visualizer': 'http://10.5.0.1:8000',
    'voting': 'http://10.5.0.1:8000',
}

# Keep ModelBackend around for per-user permissions and maybe a local
# superuser.

AUTHENTICATION_BACKENDS = [
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
]


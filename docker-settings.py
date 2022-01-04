import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType
import os

DEBUG = True

STATIC_ROOT = '/app/static/'
MEDIA_ROOT = '/app/static/media/'
ALLOWED_HOSTS = ['*']


BASEURL = os.environ.get('APP_URL')

APIS = {
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



# Modules in use, commented modules that you won't use
MODULES = [
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
           'username':  os.environ.get('DATABASE_USERNAME'),
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

# Keep ModelBackend around for per-user permissions and maybe a local
# superuser.

AUTHENTICATION_BACKENDS = [
    'django_auth_ldap.backend.LDAPBackend',
    'base.backends.AuthBackend',
]


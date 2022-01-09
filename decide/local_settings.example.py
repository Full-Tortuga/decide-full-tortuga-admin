import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

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
        'NAME': 'decide',
        'CLIENT': {
            'host': '127.0.0.1',
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

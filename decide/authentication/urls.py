from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from .views import BienvenidaView, GetUserView, LogoutView, RegisterView, LDAPLogin, SignInView, LDAPSignInView


urlpatterns = [
    path('login/', obtain_auth_token),
    path('logout/', LogoutView.as_view()),
    path('getuser/', GetUserView.as_view()),
    path('register/', RegisterView.as_view()),
    path('loginLDAP_form/', LDAPSignInView.as_view()),
    path('loginLDAP/', LDAPLogin.as_view(), name='loginldap'),
    path('login_form/', SignInView.as_view()),
    path('bienvenida/', BienvenidaView.as_view()),
]

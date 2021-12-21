from django.contrib.auth import views
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from .views import BienvenidaView, GetUserView, LogoutView, RegisterView, LDAPLogin, SignInView, cerrarsesion, LDAPSignInView

urlpatterns = [
    path('login/', obtain_auth_token),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('getuser/', GetUserView.as_view()),
    path('register/', RegisterView.as_view(), name='sign_up'),
    path('loginLDAP_form/', LDAPSignInView.as_view(), name='loginldapform'),
    path('loginLDAP/', LDAPLogin.as_view(), name='loginldap'),
    path('login_form/', SignInView.as_view(), name='sign_in'),
    path('bienvenida/', BienvenidaView.as_view()),
    path('logout/', cerrarsesion, name="logout"),
    # path('', inicio),
]

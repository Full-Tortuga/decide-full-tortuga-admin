from django.contrib.auth import views
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers

from .views import BienvenidaView, GetUserView, LogoutView, RegisterView, LDAPLogin, SignInView, cerrarsesion, LDAPSignInView
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('login/', obtain_auth_token),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('getuser/', GetUserView.as_view()),
    path('register/', RegisterView.as_view(), name='sign_up'),
    path('loginLDAP_form/', LDAPSignInView.as_view(), name='loginldapform'),
    path('loginLDAP/', LDAPLogin.as_view(), name='loginldap'),
    path('login_form/', SignInView.as_view(), name='sign_in'),
    path('bienvenida/', BienvenidaView.as_view()),
    path('userlogout/', cerrarsesion, name="userlogout"),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

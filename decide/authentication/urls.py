from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers

from .views import BienvenidaView, GetUserView, LogoutView, RegisterView, LDAPLogin, SignInView
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('login/', obtain_auth_token),
    path('logout/', LogoutView.as_view()),
    path('getuser/', GetUserView.as_view()),
    path('register/', RegisterView.as_view()),
    path('loginLDAP/', LDAPLogin.as_view()),
    path('login_form/', SignInView.as_view()),
    path('bienvenida/', BienvenidaView.as_view()),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

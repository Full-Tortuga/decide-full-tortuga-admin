from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path("", views.index, name="index"),
    path('api/users/', UsersAPI.as_view()),
    path('api/users/<int:user_id>/', UserAPI.as_view()),
    path('api/auth/login', LoginAuthAPI.as_view()),
    path('api/auth/logout', LogoutAuthAPI.as_view()),
]

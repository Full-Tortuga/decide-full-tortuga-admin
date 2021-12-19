from django.urls import path
from django.urls.conf import re_path

from . import views

urlpatterns = [
    # API
    path('api/users', views.UsersAPI.as_view()),
    path('api/users/<int:user_id>', views.UserAPI.as_view()),
    path('api/auth/login', views.LoginAuthAPI.as_view()),
    path('api/auth/logout', views.LogoutAuthAPI.as_view()),
    path('api/base/auth', views.AuthsAPI.as_view()),
    path('api/base/auth/<int:auth_id>', views.AuthAPI.as_view()),
    path('api/base/key', views.KeysAPI.as_view()),
    path('api/base/key/<int:key_id>', views.KeyAPI.as_view()),
    path('api/users/state', views.UpdateUserStateAPI.as_view()),

    # match react-app routed pages
    re_path(r'(^(?!(api)).*$)', views.index),
]

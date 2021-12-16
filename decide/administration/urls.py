from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path("", views.index, name="index"),
    path('api/users/', UsersAPI.as_view()),
    path('api/users/<int:user_id>/', UserAPI.as_view()),
    path('api/auth/login', LoginAuthAPI.as_view()),
    path('api/auth/logout', LogoutAuthAPI.as_view()),
    path('api/base/auth', AuthsAPI.as_view()),
    path('api/base/auth/<int:auth_id>/', AuthAPI.as_view()),
    path('api/base/key', KeysAPI.as_view()),
    path('api/base/key/<int:key_id>/', KeyAPI.as_view()),
    path('api/votings/question', QuestionsAPI.as_view()),
    path('api/votings/question/<int:question_id>/', QuestionAPI.as_view())
]

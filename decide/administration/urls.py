from django.conf.urls import url
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
    path('api/census', views.CensussAPI.as_view()),
    path('api/census/<int:census_id>', views.CensusAPI.as_view()),
    path('api/users/state', views.UpdateUserStateAPI.as_view()),
    path('api/votings/question', views.QuestionsAPI.as_view()),
    path('api/votings/question/<int:question_id>/', views.QuestionAPI.as_view()),
    path('api/votings/voting', views.VotingAPI.as_view()),
    # react-app
    url('', views.index)
]

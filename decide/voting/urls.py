from django.urls import path
from . import views


urlpatterns = [
    path('', views.VotingView.as_view(), name='voting'),
    path('<int:voting_id>/', views.VotingUpdate.as_view(), name='voting'),
    path('binaryVoting/', views.BinaryVotingView.as_view(), name='binaryVoting'),
    path('binaryVoting/<int:voting_id>/', views.BinaryVotingUpdate.as_view(), name='binaryVoting'),
    path('multipleVoting/', views.MultipleVotingView.as_view(), name='multipleVoting'),
    path('multipleVoting/<int:voting_id>/', views.MultipleVotingUpdate.as_view(), name='multipleVoting'),
    path('scoreVoting/', views.ScoreVotingView.as_view(), name='scoreVoting'),
    path('scoreVoting/<int:voting_id>/', views.ScoreVotingUpdate.as_view(), name='scoreVoting')
]

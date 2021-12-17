from django.urls import path
from .views import VisualizerView, Votes_csv


urlpatterns = [
    path('<int:voting_id>/', VisualizerView.as_view()),
    path('votes/<int:voting_id>/', Votes_csv.as_view()),
]

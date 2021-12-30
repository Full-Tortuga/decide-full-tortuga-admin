from django.urls import path
from .views import VisualizerView, Votes_csv, VisualizerViewBinary, VotesBinary_csv

app_name= 'visualizer'
urlpatterns = [
    path('<int:voting_id>/', VisualizerView.as_view()),
    path('votes/<int:voting_id>/', Votes_csv.as_view()),
    path('binaryVoting/<int:voting_id>/', VisualizerViewBinary.as_view()),
    path('votes/binaryVoting/<int:voting_id>/', VotesBinary_csv.as_view())
]

from django.urls import path
from .views import (GraphViewSet, VisualizerView, VisualizerViewScoring, Votes_csv, VisualizerViewBinary, VotesBinary_csv, 
VotesScoring_csv,VisualizerViewMultiple, VotesMultiple_csv, initialize, graphs_requests)


app_name= 'visualizer'
urlpatterns = [
    path('<int:voting_id>/', VisualizerView.as_view(), name='voting-simple'),
    path('votes/<int:voting_id>/', Votes_csv.as_view()),
    path('binaryVoting/<int:voting_id>/', VisualizerViewBinary.as_view()),
    path('votes/binaryVoting/<int:voting_id>/', VotesBinary_csv.as_view()),
    path('scoringVoting/<int:voting_id>/', VisualizerViewScoring.as_view()),
    path('votes/scoryVoting/<int:voting_id>/', VotesScoring_csv.as_view()),
    path('multipleVoting/<int:voting_id>/', VisualizerViewMultiple.as_view()),
    path('votes/multipleVoting/<int:voting_id>/', VotesMultiple_csv.as_view()),
    path('startTelegram/', initialize, name="start_telegram"),
    path('<int:voting_id>/graphs/', graphs_requests),
    path('graphs/', GraphViewSet.as_view({'get':'list'})),
    path('binaryVoting/<int:voting_id>/graphs/', graphs_requests),
    path('scoringVoting/<int:voting_id>/graphs/', graphs_requests),
    path('multipleVoting/<int:voting_id>/graphs/', graphs_requests),

]
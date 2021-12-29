from django.urls import path
from .views import VisualizerView, initialize, graphs_requests


urlpatterns = [
    path('<int:voting_id>/', VisualizerView.as_view()),
    path('startTelegram/', initialize, name="start_telegram"),
    path('<int:voting_id>/graphs/', graphs_requests),
]

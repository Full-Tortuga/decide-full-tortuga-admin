from django.urls import path
from .views import VisualizerView, initialize


urlpatterns = [
    path('<int:voting_id>/', VisualizerView.as_view()),
    path('startTelegram/', initialize, name="start_telegram")
]

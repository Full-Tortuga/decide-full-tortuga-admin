from django.urls import path
from .views import VisualizerView, Votes_pdf


urlpatterns = [
    path('<int:voting_id>/', VisualizerView.as_view()),
   path('votes_csv/<int:voting_id>', Votes_pdf.as_view()),
]

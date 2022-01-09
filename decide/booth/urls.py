from django.urls import path
from .views import *

app_name= 'booth'
urlpatterns = [
    path('<int:voting_id>/', BoothView.as_view()),
    path('binaryVoting/<int:voting_id>/', BinaryBoothView.as_view()),
    path('scoreVoting/<int:voting_id>/', ScoreBoothView.as_view()),
    path('multipleVoting/<int:voting_id>/', MultipleBoothView.as_view())
]

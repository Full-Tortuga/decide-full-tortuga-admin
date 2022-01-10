from django.urls import path, include
from . import backups
from . import views

urlpatterns = [
    #It isn already implemented in the views.py
    path('', views.index),
    path('create', backups.CreateBackup.as_view(), name='create_backup'),
    path('list', backups.RestoreBackup.as_view(), name='list_backups'),
    path('restore/<str:backup_name>', backups.RestoreBackup.as_view(), name='restore_backup')
]
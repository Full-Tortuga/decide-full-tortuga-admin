import os
import time
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED as ST_201,
    HTTP_400_BAD_REQUEST as ST_400,
    HTTP_404_NOT_FOUND,
)
from . import serializers

def location(dir):
  return dir + str(time.strftime("%d-%m-%Y-%Hh%Mm%Ss"))

class CreateBackup(generics.CreateAPIView):
  serializer_class = serializers.BackupSerializer
  def post(self, request, *args, **kwargs):
    try:
      print("generating mongo backup...")
      run_backup = "mongodump --out " + location("./backups/backups/")
      os.system(run_backup)
      return Response({"name": location("./backups/backups/")}, status=ST_201)
    except Exception as e:
      return Response({"error": str(e)}, status=ST_400)
    
class RestoreBackup(generics.ListCreateAPIView):
    serializer_class = serializers.BackupSerializer
    def get(self, request, *args, **kwargs):
      try:
        content = os.listdir("./backups/backups/")
        content.pop()
        return Response({"availables backups": content}, status=HTTP_200_OK)

      except Exception as e:
        return Response({"error": str(e)}, status=ST_400)
      
    def post(self, request, backup_name, *args, **kwargs):
      try:
        print("Restoring mongo backup....")
        restore_backup = "mongorestore --drop -d decide ./backups/backups/" + backup_name +"/decide"
        ls = os.listdir("./backups/backups")
        if backup_name not in ls:
           return Response({"No such file or directory"}, status=HTTP_404_NOT_FOUND)
        os.system(restore_backup)
        return Response({"Successfully backup restored "}, status=HTTP_200_OK)
      except Exception as e:
        return Response({"error": str(e)}, status=ST_400)
    




 
from django.shortcuts import render

# Create your views here.

def index(request):
    #It isnt already implemented in the views.py
    return render(request, 'backups/index.html')


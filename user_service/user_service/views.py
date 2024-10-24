# user_service/views.py

from django.shortcuts import render

def project_home(request):
    return render(request, 'home.html')

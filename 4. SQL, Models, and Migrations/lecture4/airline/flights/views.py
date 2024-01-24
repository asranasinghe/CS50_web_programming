from django.shortcuts import render
from .models import Flight
# Create your views here.

def index(request):
    return(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })
from django.http import HttpResponse
from django.shortcuts import render

def entry(request, title):
    return render(request, "wiki/entry.html", {
        "title": title
    })
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def list_profile_view(request, id=None):

    if id is None and request.user.is_authenticated:
        id = request.user.id
    elif not request.user.is_authenticated:
        id = 0

    return HttpResponse(f"<h1> Profile View - User ID: {id} </h1>", status=200) 

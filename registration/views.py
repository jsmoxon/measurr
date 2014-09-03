from django.shortcuts import render, redirect
from django.http import HttpResponse
from pg.models import *


def index(request):
    test =UserProfile.objects.get(pk=1)
    
    return HttpResponse(str(test))
    

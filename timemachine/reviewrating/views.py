from django.shortcuts import render

# Create your views here.
#views cuz gotta view it lmao

from django.http import HttpResponse
import datetime



def index(request):
	return HttpResponse("You're in review rating. AY.")
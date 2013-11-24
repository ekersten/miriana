from django.shortcuts import render
from django.http import HttpResponse

from .models import Painting

def home(request):
	return HttpResponse('Holis')
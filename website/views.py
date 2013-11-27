from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext

from moar import Thumbnailer

from .models import Painting

def home(request):
	paintings = Painting.objects.all()
	thumbnail = Thumbnailer()
	return render_to_response('website/index.html', {'paintings':paintings, 'thumbnail':thumbnail}, context_instance=RequestContext(request))
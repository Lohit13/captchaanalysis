from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.context_processors import csrf

# Create your views here.

def index(request):
	if request.method == "POST":
		print request.POST['name']
		return HttpResponse("sup")
	else:
		args = {}
		args.update(csrf(request))
		return render_to_response('index.html',args)


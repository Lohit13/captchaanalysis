from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.context_processors import csrf


import hashlib
import datetime

# Create your views here.

def image(request):
	args = {}

	if request.method == "POST":
		print request.POST["answerGiven"]

	args.update(csrf(request))
	return render_to_response("captcha.html", args)
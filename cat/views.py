from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf


import hashlib
import datetime

# Create your views here.

def index(request):
	args = {}

	try:
		done = request.session["done"]
	except:
		done = False

	try:
		hashCode = request.session["userHash"]
	except:

		# assign new hash

		hasher = hashlib.sha1()
		hasher.update(str(datetime.datetime.now()))
		request.session["userHash"] = hasher.hexdigest()
		

	if request.method == "POST":
		givenName = request.POST['name']
		
		if givenName == "":
			args["nameError"] = True
		
		else:
			request.session["name"] = request.POST['name']
			request.session["captchasDone"] = 0
			done = True
			request.session["done"] = True
			return HttpResponseRedirect("/captcha")

	if done:
		args["name"] = request.session["name"]
		args["imagesSolved"] = request.session["captchasDone"]
		args["done"] = True
	else:
		args["done"] = False

	args.update(csrf(request))
	return render_to_response('index.html',args)


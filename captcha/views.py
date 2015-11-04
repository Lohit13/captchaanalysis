from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.context_processors import csrf
from models import *

import datetime
import os

from django.conf import settings

# Create your views here.

def image(request):
	args = {}

	if request.method == "POST":
		print request.POST["answerGiven"]


	args.update(csrf(request))
	return render_to_response("captcha.html", args)


def populate(request):

	for i in range(3, 6):
		for j in range(5):
			newCase = Case(n = i, num =j)
			newCase.save()

	return HttpResponse("done")

	path = settings.PROJECT_ROOT + "/staticfiles/images"
	os.chdir(path)

	string = ""

	for i in range(1, 6):
		os.chdir(path + "/case" + str(i))
		for j in range(300):
			
			newCaptcha = Captcha()
			newCaptcha.image = str(j)

			try:
				f = open(str(j) + "_coordinates.txt")
				sol = f.readlines()

				solString = ""
				for k in sol:
					solString += (k.replace("\r\n", "") + "_")
				newCaptcha.solution = solString

				newCaptcha.case = Case.objects.get(n = len(sol), num = i)
				f.close()

				f = open(str(j) + "_question.txt")
				newCaptcha.question = f.read()
				f.close()

				newCaptcha.save()

			except:
				break

		os.chdir("..")
	return HttpResponse(string)




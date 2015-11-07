from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf

from captcha.models import *

import hashlib
import datetime
from random import randint, shuffle, choice

# Create your views here.

def index(request):
	request.session.flush()
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
			request.session["seq"] = generateRandomSequence()
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


def generateRandomSequence():

	done = False
	allImages = Captcha.objects.all()
	selectedImages = []

	cat1 = 13
	cat2 = 12
	cat3 = 12
	cat4 = 13

	sequence = ""

	for i in range(0, 5):	# cases
		
		filtered = (allImages.filter(case = Case.objects.get(num = i, n = 3)) | 
					allImages.filter(case = Case.objects.get(num = i, n = 4)) | 
					allImages.filter(case = Case.objects.get(num = i, n = 5)))

		j = 10
		while j > 0:

			try:
				newCa = choice(list(filtered))
			except:
				pass

			if newCa.cat == 0:
				if cat1 <= 0:
					pass
				else:
					print i, j
					j -= 1
					selectedImages.append(newCa)
					cat1 -= 1
					filtered = filtered.exclude(case = newCa.case, image = newCa.image)

			elif newCa.cat == 1:
				if cat2 <= 0:
					pass
				else:
					print i, j
					j -= 1
					selectedImages.append(newCa)
					cat2 -= 1
					filtered = filtered.exclude(case = newCa.case, image = newCa.image)
					
			elif newCa.cat == 2:
				if cat3 <= 0:
					pass
				else:
					print i, j
					j -= 1
					selectedImages.append(newCa)
					cat3 -= 1
					filtered = filtered.exclude(case = newCa.case, image = newCa.image)
					
			elif newCa.cat == 3:
				if cat4 <=0:
					pass
				else:
					print i, j
					j -= 1
					selectedImages.append(newCa)
					cat4 -= 1
					filtered = filtered.exclude(case = newCa.case, image = newCa.image)

	for currImage in selectedImages:
		sequence += str(currImage.image) + "," + str(currImage.case.n) + "," + str(currImage.case.num) + "," + str(currImage.cat) + "|"

	arr = sequence.split("|")[:-1]
	shuffle(arr)

	return '|'.join(arr)




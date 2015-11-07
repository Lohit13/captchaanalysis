from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from models import *

import datetime
import os
import math
import xlwt
from django.conf import settings

# seq is : image, case.n, case.num, cat|

def image(request):
	print request.session["seq"]

	args = {}

	if request.method == "POST":
		responses = request.POST["answerGiven"].split(",")
		score = 0

		print "resp : ", responses
		imageMeta = request.session["seq"].split("|")[int(request.session["captchasDone"])].split(",")
		captcha = Captcha.objects.get(image = imageMeta[0], case = Case.objects.get(n = imageMeta[1],
										   							   				num = imageMeta[2]))
		sols = captcha.solution.split("_")
		print "sols : ", sols

		for i in responses[:-1]:
			x = int(i.split("||")[0])
			y = int(i.split("||")[1])

			for j in sols[:-1]:
				ax = int(j.split("||")[0])
				ay = int(j.split("||")[1])

				if (ax - x) < 200 and (ay - y) < 200:
					score += 1
					sols.pop(sols.index(j))
					continue

		if captcha.case.num == 0:
			if captcha.case.n - score > 1:
				ans = False
			else:
				ans = True
		elif captcha.case.num == 1:
			if captcha.case.n - score > 0:
				ans = False
			else:
				ans = True	
		elif captcha.case.num == 2:
			if captcha.case.n - score > 1:
				ans = False
			else:
				ans = True	
		elif captcha.case.num == 3:
			if captcha.case.n - score - 1 > 0:
				ans = False
			else:
				ans = True	
		elif captcha.case.num == 4:
			if captcha.case.n - score - 1 > 1:
				ans = False
			else:
				ans = True				

		newTry = Run(uid = request.session['userHash'],
					 image = captcha,
					 response = request.POST["answerGiven"],
					 verdict = ans,
					 time = float(request.POST["time"]) / 1000,
					 attemptnum = request.session["captchasDone"])

		# print ans, score, captcha.case, float(request.POST["time"]) / 1000
		newTry.save()
		request.session["captchasDone"] += 1

	try:
		done = request.session["done"]
	except:
		# Hash not given yet
		return HttpResponseRedirect("/")

	if request.session["captchasDone"] > 49:
		return HttpResponseRedirect("/")

	args["captchasDone"] = request.session["captchasDone"] + 1

	imageMeta = request.session["seq"].split("|")[int(request.session["captchasDone"])].split(",")
	args["path"] = "/static/images/case" + imageMeta[2] + "/" + imageMeta[0] + ".jpg"
	args["captcha"] = Captcha.objects.get(image = imageMeta[0], 
										   case = Case.objects.get(n = imageMeta[1], num = imageMeta[2]))
	
	args["maxclicks"] = args["captcha"].case.n + 1
	
	if args["captcha"].case.num > 1:
		args["maxclicks"] -= 1

	if args["captcha"].case.num > 3:
		args["maxclicks"] -= 1

	args.update(csrf(request))
	return render_to_response("captcha.html", args)


def populate(request):

	for i in range(3, 6):
		for j in range(5):
			newCase = Case(n = i, num =j)
			newCase.save()

	path = settings.PROJECT_ROOT + "/staticfiles/images"
	os.chdir(path)

	string = ""

	for i in range(0, 5):
		print "case : ", i
		os.chdir(path + "/case" + str(i))
		for j in range(500):
			
			newCaptcha = Captcha()
			newCaptcha.image = str(j)

			f = open(str(j) + "_coordinates.txt")
			sol = f.readlines()

			solString = ""
			for k in sol:
				solString += (k.replace("\r\n", "") + "_")
			newCaptcha.solution = solString

			print "n : ", len(sol), "num : ", i
			newCaptcha.case = Case.objects.get(n = len(sol), num = i)
			f.close()

			f = open(str(j) + "_question.txt")
			newCaptcha.question = f.read()[:-8] + " images"

			f.close()

			f = open(str(j) + "_category.txt")
			newCaptcha.cat = int(f.read())
			f.close()

			newCaptcha.save()


		os.chdir("..")
	return HttpResponse(string)

def results(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename=Responses.xls'
	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet("Responses")

	row_num = 0

	columns = [
	(u"UID", 8000),
	(u"ImageNo", 8000),
	(u"Case", 8000),
	(u"Category", 8000),
	(u"AttempNo", 8000),
	(u"Time", 8000),
	(u"Verdict", 8000),
	(u"Response", 8000),
	(u"Actual Coord.", 8000),
	]

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	for col_num in xrange(len(columns)):
		ws.write(row_num, col_num, columns[col_num][0], font_style)
		ws.col(col_num).width = columns[col_num][1]

	font_style = xlwt.XFStyle()
	font_style.alignment.wrap = 1

	uids = []
	for i in Run.objects.all():
		uids.append(i.uid)

	uids = list(set(uids))

	queryset = []
	for i in uids:
		for j in Run.objects.filter(uid=i):
			queryset.append(j)
	
	for obj in queryset:
		row_num += 1
		print obj
		row = [
		    str(obj.uid),
		    str(obj.image.image),
		    str(obj.image.case.num),
		    str(obj.image.cat),
		    str(obj.attemptnum),
		    str(obj.time),
		    str(obj.verdict),
		    str(obj.response),
		    str(obj.image.solution),
		]
		for col_num in xrange(len(row)):
		    ws.write(row_num, col_num, row[col_num], font_style)
	    
	wb.save(response)
	return response


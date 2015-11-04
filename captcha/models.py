from django.db import models

# Create your models here.

class Case(models.Model):
	n = models.IntegerField(default=0)		#number of objects
	num = models.IntegerField(default=0)    #case number

	def __unicode__(self):
		return "n : " + str(self.n) + ", case : " + str(self.num)

class Captcha(models.Model):
	image = models.CharField(max_length=10)
	case = models.ForeignKey(Case)
	solution = models.TextField()
	question = models.TextField()

	def __unicode__(self):
		return "Image num : " + self.image + " case : " + str(self.case.num)

class Run(models.Model):
	uid = models.TextField()
	image = models.ForeignKey(Captcha)
	response = models.TextField()
	verdict = models.BooleanField(default=False)

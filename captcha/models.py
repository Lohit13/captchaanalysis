from django.db import models

# Create your models here.

class Case(models.Model):
	allowed = models.IntegerField(default=0)
	mininum = models.IntegerField(default=0)

class Captcha(models.Model):
	image = models.CharField(max_length=10)
	case = models.ForeignKey(Case)
	solution = models.TextField()
	question = models.TextField()

class Run(models.Model):
	uid = models.TextField()
	image = models.ForeignKey(Captcha)
	response = models.TextField()
	verdict = models.BooleanField(default=False)

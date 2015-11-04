from django.contrib import admin
from captcha.models import *

# Register your models here.

Models = [Case,Captcha,Run]

admin.site.register(Models)
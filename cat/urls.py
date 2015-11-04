from django.conf.urls import include, url
from django.contrib import admin

from captcha.views import *

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'cat.views.index', name='home'),
    url(r'^captcha/', 'captcha.views.image', name='image'),


   	
]

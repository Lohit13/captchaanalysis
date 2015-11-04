from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'cat.views.index', name='home'),

    url(r'', include('social_auth.urls')),
    url(r'^logout/', 'cat.views.logout'),

    #(r'^', include('captcha.urls')),	
]

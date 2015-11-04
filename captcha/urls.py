from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'cat.views.index', name='home'),

]

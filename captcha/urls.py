from django.conf.urls import include, url

urlpatterns = [
    url(r'^img/$', 'captcha.views.image', name='image'),
    # url(r'^populate/$', 'captcha.views.populate', name='populate'),

]

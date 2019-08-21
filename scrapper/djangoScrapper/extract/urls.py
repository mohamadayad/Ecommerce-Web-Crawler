from django.conf.urls import include,url
from . import views
urlpatterns = [
    url(r'^api$', views.api,name='api'),
    url(r'^$', views.index,name='index'),
    url(r'^contact-us$', views.contact,name='contact'),
    url(r'^how-it-works$', views.howitworks,name='howitworks'),
    url(r'^about-us$', views.aboutus,name='aboutus'),
]
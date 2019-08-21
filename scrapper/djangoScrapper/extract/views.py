from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse
from .models import scrape_data


# Create your views here.
def index(request):
	return render(request,'home.html',{})

def api(request):
	import requests
	r = requests.get(request.GET['url'],headers={'user-agent': 'Extract/0.0.1'})
	data = scrape_data(r,request)
	
	return render(request,'api.html',data)

def contact(request):
	return render(request,'contact.html',{})	

def howitworks(request):
	return render(request,'how-it-works.html',{})

def aboutus(request):
	return render(request,'about-us.html',{})
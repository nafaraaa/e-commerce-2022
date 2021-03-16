from django.shortcuts import render
from .models import Product
from django.views.generic import (
		ListView,
	)

# Create your views here.
class HomeView(ListView):
	model = Product
	template_name = 'home/indexhome.html' 
	
		
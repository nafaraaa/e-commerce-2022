from django.shortcuts import render
from .models import Product,Category
from django.views.generic import (
		ListView,
	)

# Create your views here.
class HomeView(ListView):
	model = Product
	category = Category.objects.all()
	extra_context = {
		'categories':category
	}
	def get_context_data(self):
		context = super().get_context_data()
		self.kwargs.update(self.extra_context)
		kwargs = self.kwargs
		return context
	
		
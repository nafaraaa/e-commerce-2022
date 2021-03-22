from django.shortcuts import render
from .models import Product,Category
from django.views.generic import (
		ListView,
		DetailView,
	)

# Create your views here.
class HomeView(ListView):
	model = Product
	category = Category.objects.all()
	queryset = model.objects.all()
	extra_context = {
		'categories':category
	}

	def get_queryset(self):
		if len(self.request.GET) != 0:
			self.queryset = Product.objects.filter(category_id=self.request.GET['category-id'])
		return super().get_queryset()

	def get_context_data(self):
		context = super().get_context_data()
		self.kwargs.update(self.extra_context)
		kwargs = self.kwargs
		return context

class ProductHome(DetailView):
	pass
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

# next(iter(request)) untuk mendapatkan key pertama di dictionary

	def get_queryset(self):
		request = self.request.GET
		if len(request) != 0:
			if next(iter(request)) == 'category-id':
				self.queryset = Product.objects.filter(category_id=self.request.GET['category-id'])

		return super().get_queryset()


	def get_ordering(self):
		request = self.request.GET
		if len(request) != 0:
			if next(iter(request)) == 'order':
				ordering = [request['order']]
				return ordering
		

	def get_context_data(self):
		request = self.request.GET
		context = super().get_context_data()
		self.kwargs.update(self.extra_context)
		kwargs = self.kwargs
		if len(request) != 0:
			if next(iter(request)) == 'category-id':
				context['active'] = Category.objects.get(id=self.request.GET['category-id'])
		return context

class ProductHome(DetailView):
	model = Product
	template_name = 'home/detail.html'
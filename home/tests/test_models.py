from django.test import Testcase

from home.models import Category, Product

class TesCategoryModels(Testcase):

	def setUp(self):
		self.data1 = Category.objects.create(name='django', slug='django')
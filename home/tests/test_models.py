from django.test import TestCase

from home.models import Category, Product

class TestCategoryModels(TestCase):

	def setUp(self):
		self.data1 = Category.objects.create(name='django', slug='django')

	# def test_category_model_entry(self):
	# 	print('Hai')
	# 	data = self.data1
	# 	self.assertTrue(isinstance(data, Category))
	
	def test_category_model_entry(self):
		print('Hai Kedua')
		data = self.data1
		self.assertEqual(str(data), data.name)

class TestProductModels(TestCase):
	def setUp(self):
		Category.objects.create(name='django', slug='django')
		self.data1 = Product.objects.create(category_id=1, title='Product satu',
			price='20.000', description='bleh' 
		)

	def test_product_model(self):
		print('Hai Ini Product')
		data = self.data1
		self.assertTrue(isinstance(data, Product))
		print(data)
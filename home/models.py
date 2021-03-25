from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django import forms

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(max_length=200,blank=True)
    
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    title = models.CharField(max_length=200,unique=True)
    image_product = models.ImageField(null=True, blank=True,upload_to='images/')
    price = models.DecimalField(max_digits=7,decimal_places=3)
    description = models.TextField()
    upload_time = models.DateField(auto_now_add=True)
    stock = models.IntegerField(default=1)
    slug = models.SlugField(blank= True)

    @property
    def imageURL(self):
        try:
            url = self.image_product.url
        except:
            url = ''
        return url

    def save(self):
        self.slug = slugify(self.title)
        super(Product,self).save()

    def __str__(self):
        return self.title

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank= True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL, blank=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=255, null=True)
    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, blank=True)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL, blank=True)
    quantity = models.IntegerField(default=1, null=True,blank=True) 
    date_added = models.DateTimeField(auto_now_add=True)

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL, blank=True)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL, blank=True)
    address = models.CharField(max_length=255, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address

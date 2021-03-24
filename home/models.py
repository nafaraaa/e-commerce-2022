from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django import forms

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank= True)
    name = models.CharField(max_length=255px)
    email = models.CharField(max_length=255px)
    
    def __str__(self):
        self.name


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


    def save(self):
        self.slug = slugify(self.title)
        super(Product,self).save()

    def __str__(self):
        return self.title


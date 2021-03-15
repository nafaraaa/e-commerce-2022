from django.db import models
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
    on_stock = models.BooleanField(default=True)
    slug = models.SlugField(blank= True)
    
    class Meta:
        ordering = ('-upload_time',)

    # def save(self):
    #     self.slug = slugify(self.title)
    #     super(Product,self).save()

    def __str__(self):
        return self.title


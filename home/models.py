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


class Order(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank= True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return str(self.id)

    @property
    def get_cart_totals(self):
        orderitem = self.orderitem_set.all()
        return sum([item.get_total for item in orderitem])
   
    @property
    def get_cart_items(self):
        orderitem = self.orderitem_set.all()
        return sum([item.quantity for item in orderitem])
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, blank=True)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL, blank=True)
    quantity = models.IntegerField(default=0, null=True,blank=True) 
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)

    @property
    def get_total(self):
        print(self.quantity)
        return self.product.price * self.quantity

class ShippingAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank= True)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL, blank=True)
    email = models.EmailField(max_length=200,null=True)
    kode_pos = models.IntegerField(null=True)
    kota = models.CharField(max_length=255,default='bogor')
    address = models.CharField(max_length=255, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address

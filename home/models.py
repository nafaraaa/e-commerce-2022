from django.db import models
from django.utils.text import slugify
from django.db.models.base import ModelState
from django.contrib.auth.models import User
from django.db.models.fields import NullBooleanField
import random
from django.http import JsonResponse, HttpResponseRedirect



class Category(models.Model):
    name            = models.CharField(max_length=255,unique=True)
    logo_category   = models.ImageField(null=True,blank=True,upload_to='logo/')
    slug            = models.SlugField(null=True,blank=True)

    @property
    def imageURL(self):
        try:
            url = self.logo_category.url
        except:
            url = ''
        return url

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    category        = models.ForeignKey(Category,related_name='product', on_delete=models.CASCADE)
    name            = models.CharField(max_length=255,unique=True)
    old_price       = models.DecimalField(blank=True,null=True,max_digits=8,decimal_places=3)
    price           = models.DecimalField(max_digits=8,decimal_places=3)
    description     = models.TextField()
    upload_time     = models.DateField(auto_now_add=True)
    stock           = models.IntegerField(default=1)
    slug            = models.SlugField(blank=True)

    @property
    def imageThumbnail(self):
        images = ProductImage.objects.filter(product=self.pk)
        return images[0].imageURL

    def save(self,*args,**kwargs):
        # put args for avoiding error force_insert
        self.slug = slugify(self.name)
        super(Product,self).save()

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(null=True,blank=False,upload_to='images/')

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = '/static/empty.png'
        return url

    def __str__(self):
        return self.product.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank= True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=255, null=True, unique=True)
    
    def __str__(self):
        return str(self.id)

    def save(self,*args,**kwargs):
        anjay = random.randrange(100,99999999)
        self.transaction_id = anjay
        super(Order,self).save()

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    email = models.EmailField()
    kota = models.CharField(max_length=100)
    address = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.address

    def get_absolute_url(self):
        return reverse('homey:index')
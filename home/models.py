from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.urls import reverse
import random

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    logo_category = models.ImageField(null=True, blank=True, upload_to='logo/')
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            return self.logo_category.url
        except:
            return ''

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    old_price = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=3)
    price = models.DecimalField(max_digits=8, decimal_places=3)
    description = models.TextField()
    upload_time = models.DateField(auto_now_add=True)
    stock = models.IntegerField(default=1)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def imageThumbnail(self):
        image = ProductImage.objects.filter(product=self).first()
        return image.imageURL if image else '/static/empty.png'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=False, upload_to='images/')

    def __str__(self):
        return self.product.name

    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return '/static/empty.png'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=255, null=True, unique=True)

    STATUS_CHOICES = [
        ('belum_dikirim', 'Belum Dikirim'),
        ('dikirim', 'Dikirim'),
        ('sampai', 'Sampai'),
    ]
    status_pengiriman = models.CharField(max_length=20, choices=STATUS_CHOICES, default='belum_dikirim')

    def __str__(self):
        return f"Order #{self.id}"

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = random.randrange(100, 99999999)
        super().save(*args, **kwargs)

    @property
    def get_cart_totals(self):
        return sum(item.get_total for item in self.orderitem_set.all())

    @property
    def get_cart_items(self):
        return sum(item.quantity for item in self.orderitem_set.all())

class OrderItem(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, blank=True)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product.name)

    @property
    def get_total(self):
        return self.product.price * self.quantity

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipping_user')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    email = models.EmailField(default="test@example.com")
    kota = models.CharField(max_length=100)
    address = models.TextField(default='address not filled in')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

    def get_absolute_url(self):
        return reverse('homey:index')

class Pengaduan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    judul = models.CharField(max_length=100)
    isi = models.TextField()
    tanggal = models.DateTimeField(auto_now_add=True)

    STATUS_PENGADUAN = [
        ('pending', 'Menunggu'),
        ('processing', 'Diproses'),
        ('resolved', 'Selesai'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_PENGADUAN, default='pending')

    def __str__(self):
        return f"{self.judul} - {self.status}"

from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name','slug']
	prepopulated_fields = {'slug':('name',)}

@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
	list_display = ['title','price','upload_time','slug']


@admin.register(Order)
class ProductsAdmin(admin.ModelAdmin):
	list_display = ['user','id','date_order','transaction_id']

admin.site.register(OrderItem)

@admin.register(ShippingAddress)
class ProductsAdmin(admin.ModelAdmin):
	list_display = ['user','order','address']



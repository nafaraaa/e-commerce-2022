from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name','slug']
	prepopulated_fields = {'slug':('name',)}

@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
	list_display = ['name','price','upload_time','slug']


@admin.register(Order)
class ProductsAdmin(admin.ModelAdmin):
	list_display = ['user','id','date_order','transaction_id']

admin.site.register(OrderItem)
admin.site.register(ProductImage)

@admin.register(ShippingAddress)
class ProductsAdmin(admin.ModelAdmin):
	list_display = ['user','order','address']
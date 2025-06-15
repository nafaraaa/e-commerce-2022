from django.contrib import admin
from .models import Category, Product, ProductImage, Order, OrderItem, ShippingAddress, Pengaduan

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'upload_time', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'date_order', 'complete', 'status_pengiriman']
    list_filter = ['status_pengiriman', 'complete']
    search_fields = ['transaction_id']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'order', 'quantity', 'date_added']

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product']

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'order', 'email', 'kota', 'address']

@admin.register(Pengaduan)
class PengaduanAdmin(admin.ModelAdmin):
    list_display = ['user', 'judul', 'status', 'tanggal']

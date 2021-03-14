from django.contrib import admin
from .models import Product, Category

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name','slug']
	prepopulated_fields = {'slug':('name',)}

@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
	list_display = ['title','price','upload_time','slug']


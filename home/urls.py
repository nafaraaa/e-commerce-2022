from django.urls import path
from .views import *


app_name = 'homey'
urlpatterns = [
    path('',HomeView.as_view(template_name='home/indexhome.html',paginate_by=4),name='index'),
    path('products/',HomeView.as_view(template_name='home/producthome.html',paginate_by=6),name='product'),
    path('products/<slug:slug>/',ProductDetail.as_view(template_name='home/detail.html'),name='detail'),
    path('cart/',HomeView.as_view(template_name='home/cart.html'),name="cart"),
    path('checkout/',ShippingView,name='checkout'),
    path('update-item/',updateItem, name='update-item'),
]

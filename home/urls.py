from django.urls import path,include
from.views import *

app_name = 'homey'
urlpatterns = [
    path('',HomeView.as_view(template_name='home/indexhome.html',paginate_by=4),name='index'),
    path('product/',HomeView.as_view(template_name='home/producthome.html',paginate_by=6),name='product'),
    path('product/<slug:slug>',ProdukHome.as_view(),name='detail'),
    path('cart/',HomeView.as_view(template_name='home/cart.html'),name="cart"),
    path('checkout/',ShippingView,name='checkout'),
    path('update-item/',updateItem, name='update-item'),
]

from django.urls import path,include
from.views import HomeView,ProductHome

app_name = 'homey'
urlpatterns = [
    path('',HomeView.as_view(template_name='home/indexhome.html'),name='index'),
    path('product/',HomeView.as_view(template_name='home/producthome.html'),name='product'),
    path('product/<slug:slug>',ProductHome.as_view(),name='detail'),
    path('cart/',HomeView.as_view(template_name='home/cart.html'),name="cart"),
    path('checkout/',HomeView.as_view(template_name='home/checkout.html'),name='checkout'),
]

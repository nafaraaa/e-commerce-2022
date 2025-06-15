from django.urls import path
from .views import *
from .views import (
    list_pesanan_admin, update_status_pesanan,
    list_pengaduan_admin, update_status_pengaduan,
)
from .views import ShippingView
from .views import list_pengaduan_user, tambah_pengaduan

app_name = 'homey'
urlpatterns = [
    path('', HomeView.as_view(template_name='home/indexhome.html', paginate_by=4), name='index'),
    path('products/', HomeView.as_view(template_name='home/producthome.html', paginate_by=6), name='product'),
    path('products/<slug:slug>/', ProductDetail.as_view(template_name='home/detail.html'), name='detail'),
    path('cart/', HomeView.as_view(template_name='home/cart.html'), name="cart"),
    path('checkout/', ShippingView, name='checkout'),
    path('payment-confirm/', payment_confirm, name='payment-confirm'),
    path('checkout/success/', TemplateView.as_view(template_name='home/checkout_success.html'), name='checkout-success'),
    path('payment-success/', payment_success, name='payment-success'),
    path('update-item/', updateItem, name='update-item'),
    path('admin/pesanan/', list_pesanan_admin, name='list_pesanan_admin'),
    path('admin/pesanan/update/<int:order_id>/', update_status_pesanan, name='update_status_pesanan'),
    path('pengaduan/', list_pengaduan_user, name='list_pengaduan_user'),
    path('pengaduan/tambah/', tambah_pengaduan, name='tambah_pengaduan'),  # 🧨 Tambahin ini!
    path('staff/pengaduan/', list_pengaduan_staff, name='pengaduan_staff'),
    path('staff/pengaduan/update/<int:pengaduan_id>/', update_status_pengaduan, name='update_status_pengaduan'),
]




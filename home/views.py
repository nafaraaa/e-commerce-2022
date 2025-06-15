from django.shortcuts import render, redirect
from .forms import FormShipping
from home import models
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import json
import requests
from .utils import *
from django.views.generic import (
    TemplateView,
    DetailView,
    ListView,
)
from django.contrib.admin.views.decorators import staff_member_required
from .forms import UpdateOrderStatusForm, UpdatePengaduanStatusForm
from .models import Order, Pengaduan
from .models import Pengaduan
from .decorators import staff_pengaduan_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required



class HomeView(ListView):
    models = Product
    category = Category.objects.all()
    queryset = models.objects.all()
    extra_context = {
        'categories' : category
    }
    
    def get_queryset(self):
        request = self.request.GET
        if len(request) != 0:
            if next(iter(request)) == 'category':
                self.queryset = Product.objects.filter(category_id=self.request.GET['category'])

        return super().get_queryset()

    def get_ordering(self):
        request = self.request.GET
        if len(request) != 0:
            for i in request: 
                if i == 'more-filter':
                    ordering = [request["more-filter"]]
                    return ordering

    def get_context_data(self,*args,**kwargs):
        # fakeStoreAPI()
        request = self.request
        context = super().get_context_data()
        # print("bum",context,"bum") 
        self.kwargs.update(self.extra_context)
        kwargs = self.kwargs
        for product in context["product_list"]:
            product_images = ProductImage.objects.filter(product=product.pk)
            print(product_images)
        if len(request.GET) != 0:
            if next(iter(request.GET)) == 'category-id':
                context['active'] = Category.objects.get(id=request.GET['category-id'])
        context.update(cartData(self.request))
        if context['items'] != "0":
            context.update(mergeFunction(request,context['items']))
        return context

class ProductDetail(TemplateView):
    model = Product
    def get_context_data(self,**kwargs):
        context = super().get_context_data()
        context['product'] = self.model.objects.get(slug=kwargs['slug'])

        product_images = ProductImage.objects.filter(product=context['product'].pk)
        for image in product_images:
            print(image.imageURL)

        context["prod_images"] = product_images
        exclude_object = Product.objects.exclude(slug=kwargs['slug'])
        paginator = Paginator(exclude_object,4)
        prod_list = paginator.get_page(None)
        context['product_list']=prod_list
        return context

@login_required
def ShippingView(request):
    context = {}
    form = FormShipping
    cart = cartData
    context.update(cart(request))
    if request.method == 'POST':
        form = FormShipping(request.POST)
        if form.is_valid():
            customer = request.user
            shipping,created = ShippingAddress.objects.get_or_create(
                user=customer,
                order=context['order'],
                email=request.POST.get('email'),
                kota=request.POST.get('kota'),
                address=request.POST.get('address'),
            )         
            shipping.save()
            CompleteOrder(request)
            return redirect('homey:checkout-success')
    context['form']=form
    return render(request, 'home/checkout.html', context)
print(">>> MASUK KE SHIPPING VIEW <<<")

from django.contrib import messages

@login_required
def payment_confirm(request):
    if request.method == 'POST':
        # bisa update order jadi "Menunggu Konfirmasi" kalau mau
        messages.success(request, 'Pembayaran dikonfirmasi! Order kamu akan segera diproses.')
        return redirect('homey:index')
    
def payment_success(request):
    return render(request, 'home/checkout_success.html')
  


def fakeStoreAPI():
    # This function will store data from api to django.
    responses=requests.get('https://fakestoreapi.com/products?limit=5').json()

    for response in responses:
        category = Category.objects
        obj = Product.objects.create(
            category=Category.objects.get(name=response['category']),
            name=response['title'],
            img_product1=response['image'],
            price=response['price'],
            description=response['description']
        )
        obj.save()
        # try:
        #     cat,created = Category.objects.get_or_create(name=response['category'])

        #     print('mantap gann!')
        # except:
        #     print('error gan')
    print('sipp')


@login_required
def updateItem(request):
    data = json.loads(request.body)
    print(request.body)
    productId = data['productId']
    action = data['action']
    print(productId,action,'hai')
    customer = request.user
    product = Product.objects.get(id=productId)
    order,created = Order.objects.get_or_create(user=customer, complete=False)
    orderItem,created = OrderItem.objects.get_or_create(order=order, product=product)
    if action =='add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item Was Added', safe=False)

@staff_member_required
def list_pesanan_admin(request):
    orders = Order.objects.all()
    return render(request, 'admin/orders.html', {'orders': orders})

@staff_member_required
def update_status_pesanan(request, order_id):
    order = Order.objects.get(id=order_id)
    form = UpdateOrderStatusForm(request.POST or None, instance=order)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('list_pesanan_admin')
    return render(request, 'admin/update_order.html', {'form': form})

@staff_member_required
def list_pengaduan_admin(request):
    laporan = Pengaduan.objects.all()
    return render(request, 'admin/pengaduan.html', {'laporan': laporan})

@staff_member_required
def update_status_pengaduan(request, laporan_id):
    laporan = Pengaduan.objects.get(id=laporan_id)
    form = UpdatePengaduanStatusForm(request.POST or None, instance=laporan)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('list_pengaduan_admin')
    return render(request, 'admin/update_pengaduan.html', {'form': form})

@login_required
def list_pengaduan_user(request):
    laporan = Pengaduan.objects.filter(user=request.user)
    return render(request, 'home/pengaduan_user.html', {'laporan': laporan})

@login_required
def tambah_pengaduan(request):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        isi = request.POST.get('isi')
        order_id = request.POST.get('order_id')

        Pengaduan.objects.create(
            user=request.user,
            order_id=order_id,
            judul=judul,
            isi=isi,
        )
        return redirect('list_pengaduan_user')
    
    orders = Order.objects.filter(user=request.user)
    return render(request, 'home/form_pengaduan.html', {'orders': orders})

@login_required
@staff_pengaduan_required
def list_pengaduan_staff(request):
    pengaduan = Pengaduan.objects.all().order_by('-tanggal')
    return render(request, 'home/pengaduan_list_staff.html', {'pengaduan': pengaduan})

@login_required
@staff_pengaduan_required
def update_status_pengaduan(request, pengaduan_id):
    pengaduan = get_object_or_404(Pengaduan, id=pengaduan_id)
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(Pengaduan.STATUS_PENGADUAN).keys():
            pengaduan.status = new_status
            pengaduan.save()
        return redirect('homey:pengaduan_staff')
    return render(request, 'home/update_pengaduan.html', {'pengaduan': pengaduan})
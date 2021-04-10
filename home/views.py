from django.shortcuts import render, redirect
from .models import *
from .forms import FormShipping,FormLogIn,FormSignUp
from .utils import cartData,CompleteOrder
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
import json
from django.views.generic import (
        ListView,
        DetailView,
        FormView,
        CreateView,
    )

# Create your views here.
class HomeView(ListView):
    model = Product
    category = Category.objects.all()
    queryset = model.objects.all()
    extra_context = {
        'categories':category
    }

# next(iter(request)) untuk mendapatkan key pertama di dictionary

    def get_queryset(self):
        request = self.request.GET
        if len(request) != 0:
            if next(iter(request)) == 'category-id':
                self.queryset = Product.objects.filter(category_id=self.request.GET['category-id'])

        return super().get_queryset()


    def get_ordering(self):
        request = self.request.GET
        if len(request) != 0:
            if next(iter(request)) == 'order':
                ordering = [request['order']]
                return ordering
        

    def get_context_data(self,*args,**kwargs):
        request = self.request
        context = super().get_context_data()
        self.kwargs.update(self.extra_context)
        kwargs = self.kwargs
        if len(request.GET) != 0:
            if next(iter(request.GET)) == 'category-id':
                context['active'] = Category.objects.get(id=request.GET['category-id'])
        context.update(cartData(self.request))
        return context

class ProductHome(DetailView):
    model = Product
    template_name = 'home/detail.html'

# class FormShipping(CreateView):
#     template_name = 'home/checkout.html'
#     form_class = FormShipping
#     def get_context_data(self):
#         context = super().get_context_data()
#         context.update(cartData(self.request))
#         print(context)
#         return context

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
                kode_pos=request.POST.get('kode_pos'),
                kota=request.POST.get('kota'),
                address=request.POST.get('address'),
            )         
            shipping.save()
            CompleteOrder(request)
            return redirect('homey:index')
    context['form']=form
    return render(request, 'home/checkout.html', context)

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

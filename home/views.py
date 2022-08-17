from home import models
from django.shortcuts import render
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
        # response=requests.get('https://fakestoreapi.com/products').json()
        request = self.request
        context = super().get_context_data() 
        self.kwargs.update(self.extra_context)
        kwargs = self.kwargs
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
        print(kwargs)
        context = super().get_context_data()
        exclude_object = Product.objects.exclude(slug=kwargs['slug'])
        paginator = Paginator(exclude_object,4)
        prod_list = paginator.get_page(None)
        context['product_list']=prod_list
        context['product'] = self.model.objects.get(slug=kwargs['slug'])
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
                kode_pos=request.POST.get('kode_pos'),
                kota=request.POST.get('kota'),
                address=request.POST.get('address'),
            )         
            shipping.save()
            CompleteOrder(request)
            return redirect('homey:index')
    context['form']=form
 

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
from django.shortcuts import render
from .models import *
from .forms import FormShipping,FormLogIn,FormSignUp
from .utils import cartData
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

class FormShipping(FormView):
    template_name = 'home/checkout.html'
    form_class = FormShipping

    def get_context_data(self):
        context = super().get_context_data()
        context.update(cartData(self.request))
        return context

class FormSignUp(CreateView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('homey:index')
    form_class = FormSignUp

    def get_context_data(self):
        context = super().get_context_data()
        context['judul'] = 'SignUp'
        return context

# class FormLogIn(FormView):
#     template_name = 'registration/login.html'
#     form_class = FormLogIn
#     success_url = reverse_lazy('homey:index')

#     def form_valid(self,request):
#         request = self.request.POST
#         print(request,'hai')
#         username = request['username']
#         password = request['password']
#         user = authenticate(self.request,username=username,password=password)
#         print(user)
#         return HttpResponseRedirect(self.get_success_url())

#     def get_context_data(self,*args,**kwargs):
#         context = super().get_context_data()
#         print(context)
#         context['judul'] = 'LogIn'
#         return context

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print(productId,action)
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
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views import generic

from .forms import FormSignUp,FormLogIn


def registerPage(request):
	form = FormSignUp()
	req = request.POST
	if request.method == 'POST':
		form = FormSignUp(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,'Your Account Was Created')
			user = authenticate(request,username=req['username'],password=req['password1'])
			login(request,user)
			return redirect('homey:index')
	context = {'form':form}
	return render(request, 'registration/register.html', context)

def loginPage(request):
	form = FormLogIn()
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request , username=username, password=password)

		if not user or not user.is_active:# jika bukan termasuk user atau user tidak active
			messages.error(request,'username or password not correct')
			return redirect('login')
		elif user is not None:# lain jika user tidak tidak ada (user ada :v)
			login(request,user)
			return redirect('homey:index')
	
	context = {'form':form}
	return render(request,'registration/login.html', context)

@login_required
def logoutPage(request):
	logout(request)
	return redirect('login')
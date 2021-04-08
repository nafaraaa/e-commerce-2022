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

from .forms import FormSignUp


def registerPage(request):
	form = FormSignUp()
	if request.method == 'POST':
		form = FormSignUp(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,'Your Account Was Created')
			return redirect('login')
	context = {'form':form}
	return render(request, 'registration/register.html', context)

def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request , username=username, password=password)

		if user is not None:
			login(request,user)
			return redirect('homey:index')


	context = {}
	return render(request,'registration/login.html', context)

@login_required
def logoutPage(request):
	logout(request)
	return redirect('login')
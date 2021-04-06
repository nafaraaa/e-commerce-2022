from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
	path('register/',registerPage,name='register'),
	path('login/',loginPage,name='login'),
	path('logout/',logoutPage,name='logout'),
] 

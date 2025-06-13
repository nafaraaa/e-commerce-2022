from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import *

urlpatterns = [
	path('register/',registerPage,name='register'),
	path('login/',loginPage,name='login'),
	path('logout/',logoutPage,name='logout'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('resend-verification/', views.resend_verification, name='resend_verification')
] 

from django.urls import path,include
from.views import HomeView

app_name = 'homey'
urlpatterns = [
    path('',HomeView.as_view(template_name='home/indexhome.html'),name='index'),
    path('product',HomeView.as_view(),name='product'),
]

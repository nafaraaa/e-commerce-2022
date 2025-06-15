from django import forms
from .models import Order, Pengaduan

class FormShipping(forms.Form):
    email = forms.EmailField()
    kota = forms.CharField(max_length=100)
    address = forms.CharField(widget=forms.Textarea)

class UpdateOrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status_pengiriman']

class UpdatePengaduanStatusForm(forms.ModelForm):
    class Meta:
        model = Pengaduan
        fields = ['status']
from django import forms
from .models import ShippingAddress
from django.contrib.auth.models import User

class FormShipping(forms.ModelForm):
	class Meta:
		model = ShippingAddress
		fields = [
			'email',
			'kode_pos',
			'kota',
			'address',
		]
		widgets = {
			'email':forms.TextInput(
				attrs={
					'class':'form-control',
					'placeholder':'Contoh = admincontoh@gmail.com'
				}
			),
			'kode_pos':forms.NumberInput(
				attrs={
					'class':'form-control',
				}
			),
			'kota':forms.TextInput(
				attrs={
					'class':'form-control',
				}
			),
			'address':forms.Textarea(
				attrs={
					'class':'form-control text-area',
					'placeholder':'Contoh = Taman Kenari Blok 10c No 5'
				}
			)
		}
			
class FormLogIn(forms.ModelForm):
	class Meta:
		model = User
		fields = '__all__'
			

	
		
		


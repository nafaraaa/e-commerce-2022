from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

	
class FormLogIn(forms.ModelForm):
	class Meta:
		model = User
		fields = [
			'username',
			'password'
		]
		
		widgets = {
			'username':forms.TextInput(
				attrs={
					'class':"form-control mb-3",	
				}
			),

			'password':forms.TextInput(
				attrs={
					'class':"form-control mb-3",
					'type':'password'				
				}
			)

		}

# class FormLogIn2(forms.form):
# 	username = forms.CharField(max_length=255, required=True)
#     password = forms.CharField(widget=forms.PasswordInput, required=True)

#     def clean(self):
#         username = self.cleaned_data.get('username')
#         password = self.cleaned_data.get('password')
#         user = authenticate(username=username, password=password)

#         if not user or not user.is_active:

#             raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        
#         return self.cleaned_data

#     def login(self, request):
#         username = self.cleaned_data.get('username')
#         password = self.cleaned_data.get('password')
#         user = authenticate(request, username=username, password=password)
#         return user

class FormSignUp(UserCreationForm):
	password1 = forms.CharField(
		strip=False,
		widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}),
	)

	password2 = forms.CharField(
		label=("Password confirmation"),
		widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}),
		strip=False,
		help_text=("Enter the same password as before, for verification."),
	)

	class Meta:
		model = User
		fields = (
			'username',
			'email',
			'password1',
			'password2'
		)	
		widgets = {
			'username':forms.TextInput(
				attrs={
					'class':"form-control mb-3",
				}
			),
			'email':forms.TextInput(
				attrs={
					'class':"form-control mb-3",
					'placeholder':"ex. name@gmail.com",
					'type':	'email'			
				}
			),
		}

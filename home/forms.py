from django import forms

class FormShipping(forms.Form):
    email = forms.EmailField()
    kota = forms.CharField(max_length=100)
    address = forms.CharField(widget=forms.Textarea)

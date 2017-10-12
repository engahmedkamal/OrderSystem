from django import forms
from django.contrib.auth.models import User
from .models import Order


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['first_name','last_name','username','password']


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['restaurant_name', 'menu_url']
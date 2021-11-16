from django import forms
from django.forms import ModelForm
from .models import Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class RegisterForm(forms.Form):
    username = forms.CharField(label='Your name')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput, label='Password confirmation'
    )
    email = forms.EmailField(label='Your email')

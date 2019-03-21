from django.forms import ModelForm
from .models import Event, User
from django import forms

class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
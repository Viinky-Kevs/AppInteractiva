from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUser(UserCreationForm):
	
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1','password2']

class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
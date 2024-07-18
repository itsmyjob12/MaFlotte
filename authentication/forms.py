from django import forms
from django.contrib.auth.forms import UserCreationForm
from  authentication.models import User
from django import forms
from .models import Profile
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import SetPasswordForm


User = get_user_model()


class FirstLoginPasswordChangeForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))

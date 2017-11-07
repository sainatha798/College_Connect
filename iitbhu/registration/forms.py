__author__ = 'sainatha798'
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Userinfo
from django.forms import  ModelForm
class Signup(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    username = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    email = forms.EmailField(required=True)
    ##confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class Login(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class ContactForm(forms.Form):
    Subject = forms.CharField(max_length=50)
    Message = forms.CharField(widget=forms.Textarea)

class Userinfo(ModelForm):

    profile_picture = forms.FileField(required=None)
    dob = forms.DateField(required=None,widget=forms.DateInput,label='Date of Birth')
    class Meta:
        model = Userinfo
        fields = ['mobile_no','profile_picture','dob']

class Change_password(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput, label='New Password')
    new_password1 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')


##class EditProfile()

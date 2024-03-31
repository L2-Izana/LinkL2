from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    sex = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    email = forms.EmailField()
    

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'sex', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    sex = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], required=False)
    email = forms.EmailField(required=False)
    username = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'sex', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        

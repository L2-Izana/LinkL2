from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Avatar

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    sex = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'sex', 'email', 'password1', 'password2']


class UserProfileAvatarUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['sex', 'curr_work', 'highest_education', 'curr_place', 'phone_contact', 'social_link', 'relationship']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'] = forms.ImageField(required=False)
        

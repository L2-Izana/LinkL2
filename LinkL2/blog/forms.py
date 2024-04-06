from django import forms
from .models import Post

class PostCreateUpdateForm(forms.ModelForm):
    title = forms.CharField(required=False)
    content = forms.CharField(required=False, widget=forms.Textarea)
    image = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'image']

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, UserProfileAvatarUpdateForm
from django.http import HttpResponse
from pprint import pprint
from django.views.generic import DetailView, UpdateView, ListView
from .models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from blog.models import Post

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
        messages.add_message(request, messages.INFO, 'Fill out the registration form below to create an account.', extra_tags='persistent')
    return render(request, 'users/register.html', {'form': form})

class UserProfileView(DetailView):
    model = Profile

    def get_object(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return get_object_or_404(Profile, user=user)

class UserProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = UserProfileAvatarUpdateForm

    def get_object(self):
        return get_object_or_404(Profile, user__username=self.kwargs.get('username'))

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        updated_image = self.request.FILES.get('image')
        if updated_image:
            instance.avatar.image = updated_image
        instance.save()
        instance.avatar.save()
        return super().form_valid(form)
    
    def test_func(self):
        profile = self.get_object()
        return profile.user == self.request.user

    def get_success_url(self):
        return reverse_lazy('user-profile', kwargs={'username': self.kwargs.get('username')})

class UserPhotosListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "users/user_photos.html"
    context_object_name = 'posts'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['viewing_user'] = get_object_or_404(User, username=self.kwargs.get('username'))
        return context

def photos(request, username):
    return HttpResponse("Photos view of user")

def friends(request, username):
    return HttpResponse("Friends view of user")

def videos(request, username):
    return HttpResponse("Videos view of user")
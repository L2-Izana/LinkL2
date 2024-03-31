from typing import Any
from django.contrib.auth.models import User
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from .models import Post, React, PostImage
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
    )
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import PostUploadForm
from django.contrib import messages
import pprint
from .models import React, Comment

# Home page - CBV
class PostListView(LoginRequiredMixin, ListView):
    upload_post = False

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
    
    model = Post
    template_name = "blog/home.html"
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3

    def get_latest_reacts(self, user, posts):
        latest_reacts_dict = {}
        for post in posts:
            latest_react = React.objects.filter(user=user, post=post).order_by('-timestamp').first()
            if latest_react is not None:
                latest_reacts_dict[post] = latest_react.reaction
            else:
                latest_reacts_dict[post] = None
        return latest_reacts_dict

    def get_comments_dict(self):
        comments_dict = {} # In form of: {post:[(user1, comment), (user2, comment), ...]}
        comment_queryset = Comment.objects.all()
        for comment_query in comment_queryset:
            curr_post = comment_query.post
            curr_user = comment_query.user
            curr_comment = comment_query.comment
            if curr_post not in comments_dict:
                comments_dict[curr_post] = [(curr_user, curr_comment)]
            else:
                comments_dict[curr_post].append((curr_user, curr_comment))
        return comments_dict
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upload_post'] = self.upload_post
        if self.upload_post:
            context['post_upload_form'] = PostUploadForm()
        context['latest_reacts_dict'] = self.get_latest_reacts(self.request.user, self.object_list)
        context['comments_dict'] = self.get_comments_dict()
        return context
    
    def post(self, request, *args, **kwargs):
        post_uploaded_form = PostUploadForm(request.POST, request.FILES)
        if post_uploaded_form.is_valid():
            new_post = post_uploaded_form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('blog-home')
        else:
            return redirect('upload-post')


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blog/user_posts.html"
    context_object_name = 'posts'
    paginate_by = 3
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
    
    def get_latest_reacts(self, user, posts):
        latest_reacts_dict = {}
        for post in posts:
            latest_react = React.objects.filter(user=user, post=post).order_by('-timestamp').first()
            if latest_react is not None:
                latest_reacts_dict[post] = latest_react.reaction
            else:
                latest_reacts_dict[post] = None
        return latest_reacts_dict

    def get_comments_dict(self):
        comments_dict = {} # In form of: {post:[(user1, comment), (user2, comment), ...]}
        comment_queryset = Comment.objects.all()
        for comment_query in comment_queryset:
            curr_post = comment_query.post
            curr_user = comment_query.user
            curr_comment = comment_query.comment
            if curr_post not in comments_dict:
                comments_dict[curr_post] = [(curr_user, curr_comment)]
            else:
                comments_dict[curr_post].append((curr_user, curr_comment))
        return comments_dict
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        viewing_user=get_object_or_404(User, username=self.kwargs.get('username'))
        context['latest_reacts_dict'] = self.get_latest_reacts(viewing_user, self.object_list)
        context['comments_dict'] = self.get_comments_dict()
        context['viewing_user'] = viewing_user
        return context


def save_reaction(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        post_id = request.POST.get('post_id')
        reaction_type = request.POST.get('reaction')
        react = React(user_id = user_id, post_id = post_id, reaction = reaction_type)
        react.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})
    

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post  

    def get_object(self, queryset=None):
        uuid = self.kwargs.get('id')
        return get_object_or_404(Post, id=uuid)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content', 'image']
    success_url = reverse_lazy('blog-home')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.save()
        PostImage(post=instance, image=self.request.FILES.get('image')).save()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.save()
        updated_image = self.request.FILES.get('image')
        if instance.postimage.image:
            instance.postimage.delete()
        if updated_image:
            PostImage(post=instance, image=updated_image).save()
        return super().form_valid(form)

    def get_object(self, queryset=None):
        uuid = self.kwargs.get('id')
        return get_object_or_404(Post, id=uuid)

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog-home')

    def get_object(self, queryset=None):
        uuid = self.kwargs.get('id')
        return get_object_or_404(Post, id=uuid)

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

# About page
def about(request):
    return render(request, 'blog/about.html', context={'title': 'About'})
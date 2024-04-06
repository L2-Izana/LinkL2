from typing import Any
from django.contrib.auth.models import User
from django.db.models.base import Model as Model
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
from .forms import PostCreateUpdateForm
from .models import React, Comment
from sidebar.models import Notification


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
        comments_dict = {} 
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
        context['latest_reacts_dict'] = self.get_latest_reacts(self.request.user, self.object_list)
        context['comments_dict'] = self.get_comments_dict()
        context['notification_count'] = Notification.objects.filter(receiving_user=self.request.user, is_read=False).count()
        return context


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
        context['notification_count'] = Notification.objects.filter(receiving_user=self.request.user, is_read=False).count()
        return context
    

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post  

    def get_object(self, queryset=None):
        uuid = self.kwargs.get('id')
        return get_object_or_404(Post, id=uuid)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notification_count'] = Notification.objects.filter(receiving_user=self.request.user, is_read=False).count()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateUpdateForm
    success_url = reverse_lazy('blog-home')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.save()
        PostImage(post=instance, image=self.request.FILES.get('image')).save()
        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notification_count'] = Notification.objects.filter(receiving_user=self.request.user, is_read=False).count()
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostCreateUpdateForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.save()
        updated_image = self.request.FILES.get('image')
        instance.postimage.image = updated_image
        return super().form_valid(form)

    def get_object(self, queryset=None):
        uuid = self.kwargs.get('id')
        return get_object_or_404(Post, id=uuid)

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notification_count'] = Notification.objects.filter(receiving_user=self.request.user, is_read=False).count()
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog-home')

    def get_object(self, queryset=None):
        uuid = self.kwargs.get('id')
        return get_object_or_404(Post, id=uuid)

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notification_count'] = Notification.objects.filter(receiving_user=self.request.user, is_read=False).count()
        return context

def about(request):
    return render(request, 'blog/about.html', context={'title': 'About'})


def save_reaction(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        post_id = request.POST.get('post_id')
        reaction_type = request.POST.get('reaction')
        react = React(user_id = user_id, post_id = post_id, reaction = reaction_type)
        react.save()
        reacted_post = Post.objects.get(id=post_id)
        sending_user = request.user
        receiving_user = reacted_post.author
        Notification.objects.create(sending_user=sending_user, receiving_user=receiving_user, notification_type='Blog-react', post=reacted_post, reaction=reaction_type)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})
    
def share_post(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        post_id = request.POST.get('post_id')
        shared_post = Post.objects.get(id=post_id)
        new_post = Post.objects.create(
            author = User.objects.get(id=user_id),
            title = shared_post.title,
            content = shared_post.content
        )
        new_post.save()
        if hasattr(shared_post, 'postimage'):
            PostImage.objects.create(post=new_post, image=shared_post.postimage.image).save()
        Notification.objects.create(sending_user=request.user, receiving_user=shared_post.author, notification_type='Blog-share', post=shared_post)
        return JsonResponse({'status': 'success'})
    else:
        print('share_post API accessed')
        return JsonResponse({'status': 'error'})

def check_notification(request):
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        checked_notification = Notification.objects.get(id=notification_id)
        checked_notification.is_read = True
        checked_notification.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})
    
def upload_comment(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        post_id = request.POST.get('post_id')
        comment_content = request.POST.get('comment_content')
        Comment.objects.create(user_id=user_id, post_id=post_id, comment=comment_content)
        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "error"})
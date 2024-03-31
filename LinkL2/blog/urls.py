from django.urls import path
from . import views
from .views import (
    PostListView, 
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
    )

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<str:id>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<str:id>/detail/', PostDetailView.as_view(), name='post-detail'),
    path('post/<str:id>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about')
]
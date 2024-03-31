from django.urls import path
from . import views
from blog.views import UserPostListView

urlpatterns = [
    path('<str:username>/posts/', UserPostListView.as_view(), name='user-posts'),
    path('<str:username>/profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('<str:username>/profile/update', views.UserProfileUpdateView.as_view(), name='profile-update'),
    path('<str:username>/photos', views.UserPhotosListView.as_view(), name="user-photos"),
    path('<str:username>/friends', views.friends, name="user-friends"),
    path('<str:username>/videos', views.videos, name="user-videos")    
]

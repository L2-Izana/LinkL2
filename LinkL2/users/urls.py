from django.urls import path
from . import views
import blog.views as blog_views
import users.views as user_views
import sidebar.views as sidebar_views
urlpatterns = [
    path('<str:username>/posts/', blog_views.UserPostListView.as_view(), name='user-posts'),
    path('<str:username>/profile/', user_views.UserProfileView.as_view(), name='user-profile'),
    path('<str:username>/profile/update/', user_views.UserProfileUpdateView.as_view(), name='profile-update'),
    path('<str:username>/photos/', user_views.UserPhotosListView.as_view(), name="user-photos"),
    path('<str:username>/friends/', user_views.friends, name="user-friends"),
    path('<str:username>/videos/', user_views.videos, name="user-videos"),
    path('<str:username>/notifications/', sidebar_views.UserNotificationsView.as_view(), name='user-notifications'),
    path('<str:username>/tasks/', user_views.tasks, name='user-tasks')    
]

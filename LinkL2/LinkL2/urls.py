"""
URL configuration for LinkL2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views
from blog import views as blog_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # User Authentication
    path('', RedirectView.as_view(pattern_name='login'), name='home'),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    
    # App Features
    path('blog/', include('blog.urls')),
    path('users/', include('users.urls')),

    # API
    path('blog/api/save_reaction/', blog_views.save_reaction, name='save-reaction'),
    path('blog/api/share_post/', blog_views.share_post, name='share-post'),
    path('api/check_notification/', blog_views.check_notification, name='check-notification'),
    path('api/upload_comment/', blog_views.upload_comment, name='upload-comment')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\
 + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

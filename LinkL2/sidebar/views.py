from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from django.contrib.auth.models import User
from .models import Notification


class UserNotificationsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Notification
    template_name = "sidebar/user_notifications.html"
    context_object_name = 'notifications'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Notification.objects.filter(receiving_user=user).order_by

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        viewing_user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['viewing_user'] = viewing_user
        context['object'] = viewing_user.profile
        return context
    
    def test_func(self):
        return self.kwargs.get('username') == self.request.user.username
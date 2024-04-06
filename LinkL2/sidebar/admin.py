from django.contrib import admin
from .models import Notification, Task

admin.site.register(Notification)
admin.site.register(Task)
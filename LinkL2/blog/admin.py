from django.contrib import admin
from .models import Post, React, Comment, PostImage

# Register models
admin.site.register(Post)
admin.site.register(React)
admin.site.register(Comment)
admin.site.register(PostImage)
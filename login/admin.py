from django.contrib import admin

from .models import Comment, User, Wall_Message

admin.site.register(User)
admin.site.register(Wall_Message)
admin.site.register(Comment)

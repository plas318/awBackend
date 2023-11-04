from django.contrib import admin
from .models import CustomUser, Post, Comment, Category, Tag
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Tag)

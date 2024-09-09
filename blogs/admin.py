# blogs/admin.py

from django.contrib import admin
from .models import BlogPost, Tag

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    #prepopulated_fields = {'slug': ('title',)}
    list_filter = ('author', 'tags')
    search_fields = ('title', 'content')
    ordering = ['-created_at']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

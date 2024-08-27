from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'parent', 'created_at', 'is_reply')
    list_filter = ('created_at', 'author')
    search_fields = ('author__username', 'content')
    ordering = ('-created_at',)
    raw_id_fields = ('post', 'author', 'parent')  # For better performance with large datasets

    def is_reply(self, obj):
        return obj.is_reply
    is_reply.boolean = True  # Display as a boolean icon in the admin list view

admin.site.register(Comment, CommentAdmin)

from django.contrib import admin
from .models import Buzz

class BuzzAdmin(admin.ModelAdmin):
    list_display = ('user', 'trigger', 'post', 'comment', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'trigger__username', 'post__title', 'comment__content')

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected buzzes as read"

    actions = [mark_as_read]

admin.site.register(Buzz, BuzzAdmin)

'''
list_display: This tuple defines the fields displayed in the list view of the Buzz model in the admin interface. This makes it easy to see key information at a glance, such as the user, trigger, post, comment, read status, and the creation date.

list_filter: This tuple allows filtering buzzes by is_read status and created_at date in the admin interface, making it easier to manage the notifications.

search_fields: This tuple enables searching through the buzzes by user’s username, trigger’s username, post title, and comment content, improving the admin interface's usability.

mark_as_read: This method defines a custom admin action that allows you to mark multiple buzzes as read. It updates the is_read field to True for the selected buzzes.

actions: This list includes the mark_as_read action in the admin interface, so you can apply it to selected items.
'''
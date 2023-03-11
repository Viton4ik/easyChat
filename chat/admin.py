
from django.contrib import admin

from .models import Chat, Message, UserProfile


class ChatAdmin(admin.ModelAdmin):
    """ Admin panel upgrade """
    list_display = ('id', 'name', )
    search_fields = ('name', )
    list_filter = ('name', )


class MessageAdmin(admin.ModelAdmin):
    """ Admin panel upgrade """
    list_display = [field.name for field in Message._meta.get_fields()]


class UserProfileAdmin(admin.ModelAdmin):
    """ Admin panel upgrade """
    list_display = ('id', 'user', 'avatar', )


admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

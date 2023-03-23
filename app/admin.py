from django.contrib import admin
from .models import Group,Messages

class GroupAdmin(admin.ModelAdmin):
    list_display = ['name','user1','user2']

admin.site.register(Group, GroupAdmin)


class MessagesAdmin(admin.ModelAdmin):
    list_display = ['content','user','group']

admin.site.register(Messages, MessagesAdmin)

    

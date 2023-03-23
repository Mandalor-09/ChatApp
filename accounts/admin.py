from django.contrib import admin

# Register your models here.
from .models import Friend
class FriendModel(admin.ModelAdmin):
    list_display=['id','user']

admin.site.register(Friend,FriendModel)
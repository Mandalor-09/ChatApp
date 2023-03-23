from django.db import models
from accounts.models import BaseModel
from django.contrib.auth.models import User


class Group(BaseModel):
    name = models.CharField(max_length=100)
    user1 = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user1')
    user2 = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user2')

    def __str__(self) -> str:
        return self.name

class Messages(BaseModel):
    group = models.ForeignKey(Group,on_delete=models.CASCADE,related_name='group')
    content = models.CharField(max_length=1000)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')

    def __str__(self) -> str:
        return self.content
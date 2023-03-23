from django.db import models
import uuid
from django.contrib.auth.models import User



class BaseModel(models.Model):
    uid = models.CharField(max_length=100,default=uuid.uuid4,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Friend(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='friend')
    friends = models.ManyToManyField(User,blank=True,related_name='friends_of')

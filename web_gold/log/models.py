from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class LOG(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    content = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True,blank=False,null=False)
from django.db import models
from django.contrib.auth.models import User
from django_mysql.models import JSONField
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    location = models.CharField(max_length=50,default="Warsaw")
    
class Favourite(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    my_favourite = JSONField()
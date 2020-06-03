from django.db import models
from django.contrib.auth.models import User
from django_mysql.models import JSONField
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    location = models.CharField(max_length=100,default="Warsaw")
    
class Places(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    my_places = JSONField()

class Favourites(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    my_favourites = JSONField()

class Rejected(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    my_rejected = JSONField()
from django.db import models
from django.contrib.auth.models import User


# Vulnerability (validation should be stricter)
class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    starting_price = models.IntegerField()
    current_bid = models.IntegerField()
    min_increment = models.IntegerField()
    location = models.TextField()
    expiration_time = models.DateTimeField()
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_owner'
    )
    bidder = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_bidder'
    )


# Vulnerability (validation should be stricter)
class UserData(models.Model):
    id = models.AutoField(primary_key=True)
    funds = models.IntegerField()
    reserved_funds = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)


# Vulnerability (validation should be stricter)
class Log(models.Model):
    id = models.AutoField(primary_key=True)
    path = models.TextField()
    params = models.TextField()
    remote_addr = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

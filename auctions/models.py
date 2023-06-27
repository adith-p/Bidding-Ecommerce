from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Catagory(models.Model):
    catagory_name = models.CharField(max_length=30, blank=True)

    def __str__(self) -> str:
        return self.catagory_name


class Bids(models.Model):
    bid = models.FloatField(blank=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ownerUser')

    def __str__(self) -> str:
        return f"{self.user}"


class Auction_list(models.Model):
    title = models.CharField(max_length=30, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    image_url = models.CharField(max_length=1000, blank=True, null=True)
    desc = models.TextField(max_length=3000, null=False)
    bid = models.ForeignKey(
        Bids, on_delete=models.CASCADE, related_name='userBids', )

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ownerAuction', )
    is_active = models.BooleanField(default=True)
    catagory = models.ForeignKey(
        Catagory, on_delete=models.CASCADE, related_name="cat", default=" ")

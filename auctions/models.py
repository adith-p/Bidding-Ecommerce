from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Catagory(models.Model):
    catagory_name = models.CharField(max_length=30, blank=True,)

    def __str__(self) -> str:
        return self.catagory_name


class Bids(models.Model):
    bid = models.FloatField(blank=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ownerUser')

    bid_time = models.DateTimeField(auto_now=True)

    auction_id = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.id}"


class Auction_list(models.Model):
    title = models.CharField(max_length=30, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    image_url = models.CharField(
        max_length=1000, blank=True, null=True)
    desc = models.TextField(max_length=3000, null=False)
    bid = models.ForeignKey(
        Bids, on_delete=models.CASCADE, related_name='userBids', )

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ownerAuction')
    is_active = models.BooleanField(default=True)
    catagory = models.ForeignKey(
        Catagory, on_delete=models.CASCADE, related_name="cat", default=" ", null=True)

    class Meta:
        ordering = ['-created_on']


class Bookmarks(models.Model):
    auction_id = models.ForeignKey(
        Auction_list, on_delete=models.CASCADE, related_name="bookmark")
    bookmarks = models.ManyToManyField(
        User, blank=True, null=True, related_name="bookmark_id")

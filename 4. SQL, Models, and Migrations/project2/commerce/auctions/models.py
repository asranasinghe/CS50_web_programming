from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_hist")

    def __str__(self):
        return f"{self.title}: ${self.price} [{self.owner}]."


class bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidding_hist")
    listing = models.ForeignKey(listing, on_delete=models.CASCADE, related_name="bids")
    price = models.FloatField()

    def __str__(self):
        return f"{self.bidder}: Bid ${self.price} for {self.listing}"


class comment(models.Model):
    text = models.TextField()
    listing = models.ForeignKey(listing, on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.name} commented: {self.text}"

from django.contrib.auth.models import AbstractUser
from django.db import models
CATEGORY_CHOICES = [
    ("Fashion", "Fashion"),
    ("Toys", "Toys"),
    ("Electronics", "Electronics"),
    ("Home", "Home"),
    ("Other", "Other"),
    ("all","all")
]

class User(AbstractUser):
    pass

class Listings(models.Model):
    title =models.CharField(max_length=100)
    description = models.TextField()
    starting_bid =models.DecimalField(max_digits=10, decimal_places=2)
    image_url =models.URLField()
    create_at =models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    status =models.TextField(default="ongoing")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True, null=True)



    def __str__(self):
        return self.title
    
class Watchlists(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    item = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="watchlisted_by")

    class Meta:
        unique_together = ("user", "item")  # Prevents duplicate watchlist entries

    def __str__(self):
        return f"{self.user.username} - {self.item.title}"
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlists")
    # item = models.ForeignKey(Listings, on_delete=models.CASCADE)

class Bidding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Bidding")
    new_bidding=models.DecimalField(max_digits=10, decimal_places=2)
    item = models.ForeignKey(Listings, on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.listing.title}"
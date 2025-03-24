from django.contrib import admin
from .models import Listings, Bidding, Comment

# Optional: Customize how models display in admin
class ListingsAdmin(admin.ModelAdmin):
    list_display = ('title', 'starting_bid', 'status', 'category')
    search_fields = ('title', 'category', 'description')

class BiddingAdmin(admin.ModelAdmin):
    list_display = ('item', 'user', 'new_bidding')
    search_fields = ('item__title', 'user__username')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'timestamp')
    search_fields = ('user__username', 'listing__title', 'content')

# Register your models
admin.site.register(Listings, ListingsAdmin)
admin.site.register(Bidding, BiddingAdmin)
admin.site.register(Comment, CommentAdmin)

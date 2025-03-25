from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django import forms
from .models import User,Listings,Watchlists,Bidding,Comment
from django.shortcuts import render, redirect
from .forms import Listings_Form,Biding_form,Watchlist_form,close_form,CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Max
def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

# def active_list(request):
#     listings = Listings.objects.all() # ✅ Get all listings from the database
#     biddings = Bidding.objects.all()
#     return render(request, "auctions/index.html", {
#         "listings": listings  # ✅ Pass listings to template
#         "biddings": biddings
#     })

def active_list(request):
    listings = Listings.objects.all()  # Get all listings
    highest_bids = Bidding.objects.values('item').annotate(max_bid=Max('new_bidding'))   # Get highest bids per item

    return render(request, "auctions/index.html", {
        "listings": listings,  # Pass listings to template
        "highest_bids": highest_bids  # Pass highest bids for each listing
    })

# def listings(request,id):
#     item = get_object_or_404(Listings, id=id) 
#     item_user=get_object_or_404(User,username=item.user.username)
#     usernamep=item_user.username
#     highest_bid = Bidding.objects.filter(item=item).aggregate(Max('new_bidding'))['new_bidding__max'] or item.starting_bid
#     currentbid=highest_bid

#     comment_form = CommentForm()
#     you_bid=None
#     if request.user==item.user and item.status=="ongoing":
#         if request.method == 'POST':
#             closeform = close_form(request.POST)
#             if closeform.is_valid():
#                 item.status="close"
#                 item.save()
#                 messages.success(request, "Closed auction!")
#             else:
#                 messages.warning(request, "Auction already Closed")
#         else:
#             closeform = close_form()
            
#         return render(request, "auctions/listings.html", {
#             "item": item,
#             'username':usernamep,
#             'currentbid':currentbid,
#             'you_bid':you_bid,
#             "closeform":closeform
#         })
#     elif 'submit_comment' in request.POST:
#             comment_form = CommentForm(request.POST)
#             if comment_form.is_valid():
#                 comment = comment_form.save(commit=False)
#                 comment.user = request.user
#                 comment.listing = item
#                 comment.save()
#                 return redirect("listings", id=id)
            
#     elif item.status=="close":
#         return render(request, "auctions/listings.html", {
#             "item": item,
#             'username':usernamep,
#             'currentbid':currentbid,
#             'you_bid':you_bid,
#             "close":"closed"

#         })
    
#     else:
#         return render(request, "auctions/listings.html", {
#             "item": item,
#             'username':usernamep,
#             'currentbid':currentbid,
#             'you_bid':you_bid,
#         })

def listings(request, id):
    item = get_object_or_404(Listings, id=id)
    item_user = item.user  # Directly use item.user
    usernamep = item_user.username

    # Get the highest bid or default to starting bid
    highest_bid = Bidding.objects.filter(item=item).aggregate(Max('new_bidding'))['new_bidding__max'] or item.starting_bid
    currentbid = highest_bid

    # Track if the user has bid before
    you_bid = Bidding.objects.filter(item=item, user=request.user).exists() if request.user.is_authenticated else None

    # Forms
    comment_form = CommentForm()
    closeform = close_form()

    # Handle closing the auction (if the owner submits)
    if request.user == item.user and item.status == "ongoing" and request.method == 'POST' and 'close_auction' in request.POST:
        closeform = close_form(request.POST)
        if closeform.is_valid():
            item.status = "close"
            item.save()
            messages.success(request, "Closed auction!")
            return redirect("listings", id=id)
    
    # Handle comment submission
    if request.user.is_authenticated and 'submit_comment' in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.listing = item
            comment.save()
            return redirect("listings", id=id)

    # Render the correct template based on auction status
    context = {
        "item": item,
        "username": usernamep,
        "currentbid": currentbid,
        "you_bid": you_bid,
        "comment_form": comment_form,
        "closeform": closeform,
        "close": "closed" if item.status == "close" else None
    }
    return render(request, "auctions/listings.html", context)

def create_listings(request):
    if not request.user.is_authenticated:  # ✅ Check if user is logged in
        messages.error(request, "⚠️ Please login to create a listing.")  # ✅ Show message
        return render(request, "auctions/login.html")  # ✅ Stay on same page
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Listings_Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            new_listing = Listings(
            title=form.cleaned_data['title'],
            description=form.cleaned_data['description'],
            starting_bid=form.cleaned_data['starting_bid'],
            image_url=form.cleaned_data['image_url'],
            category = form.cleaned_data['category']

            )
            new_listing.user = request.user
            new_listing.save()  # Save to the database
    
            return HttpResponseRedirect(reverse("index"))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Listings_Form()

    return render(request, "auctions/create_listings.html",{"form": form})



# def biddings(request, id):
#     if not request.user.is_authenticated:  # ✅ Check if user is logged in
#         messages.error(request, "⚠️ Please login to auctions.")  # ✅ Show message
#         return render(request, "auctions/login.html")  # ✅ Stay on same page
    
#     item = get_object_or_404(Listings, id=id) 
#     item_user=get_object_or_404(User,id=request.user.id)
#     item_username=item_user.username
#     usernamep=item_username
#     highest_bid = Bidding.objects.filter(item=item).aggregate(Max('new_bidding'))['new_bidding__max'] or item.starting_bid
#     currentbid=highest_bid

    
#     if request.user==get_object_or_404(Bidding,new_bidding=highest_bid).user:
#         you_bid="you bid is the current bid"
#     else:
#         you_bid=None
                
#     if request.method == 'POST':
#         form = Biding_form(request.POST)  
        
#         if form.is_valid():
#             new_bid = form.cleaned_data['starting_bid']  
            
            
#             if new_bid > item.starting_bid and new_bid > highest_bid:
#                 new_bidding=Bidding(
#             new_bidding=form.cleaned_data['starting_bid'],
#             )
#                 new_bidding.item=item
#                 new_bidding.user=request.user
#                 new_bidding.save()
#                 return redirect("listings", id=id)  
#             else:
#                 return render(request, "auctions/listings.html", {
#                     "form": form,
#                     "item": item,
#                     'username':usernamep,
#                     "error": "Bid must be higher than the current price!",
#                     'currentbid':currentbid,
#                     'you_bid':you_bid
#                 })
    
#     else:
#         form = Biding_form() 
#     return render(request, "auctions/listings.html", {
#         "form": form,
#         "item": item,
#         'username':usernamep,
#         'currentbid':currentbid,
#         'you_bid':you_bid
#     })

# def watchlist(request):
#     user = request.user
#     if not user.is_authenticated:
#         return render(request, "auctions/watchlist.html", {
#             "message": "You must be logged in to view your Watchlist."
#         })

#     all_items = Watchlists.objects.filter(user=user)  # Use filter instead of direct FK lookup

#     return render(request, "auctions/watchlist.html", {
#         "all": all_items,
#         "message": "You do not have a Watchlist" if not all_items.exists() else None
#     })
# def submit_status(request):
#     if request.method == "POST":
#         form = Watchlist_form(request.POST)
#         if form.is_valid():
#             status_value = form.cleaned_data["status"]  # Always "Submitted"
#             new_watchlist=Watchlists
#             new_watchlist.item=itemid
#             new_watchlist.user=request.user
            
           
#     else:
#         form = Watchlist_form()

def add_to_watchlist(request, item_id):
    item = get_object_or_404(Listings, id=item_id)

    if request.method == "POST":
        form = Watchlist_form(request.POST)
        if not Watchlists.objects.filter(user=request.user, item=item).exists():
            Watchlists.objects.create(user=request.user, item=item)
            messages.success(request, "Item added to watchlist!")
        else:
            messages.warning(request, "This item is already in your watchlist!")

    return redirect("index")

# def watchlist(request):
#     watchlistitem = Watchlists.objects.filter(user=request.user)  
#     listings = Listings.objects.filter(user=watchlistitem.user,id=watchlistitem.item)

#     return render(request, "auctions/Watchlist.html", {
#         "listings": listings,  
        
#     })
    
def watchlist(request):
    
    watchlist_items = Watchlists.objects.filter(user=request.user)

    item_ids = watchlist_items.values_list("item__id", flat=True)  

    listings = Listings.objects.filter(id__in=item_ids)

    return render(request, "auctions/Watchlist.html", {
        "listings": listings,  
    })

def remove_from_watchlist(request, item_id):
    item = get_object_or_404(Listings, id=item_id)

    if request.method == "POST":
        form = Watchlist_form(request.POST)
        if Watchlists.objects.filter(user=request.user, item=item).exists():
            Watchlists.objects.filter(user=request.user, item=item).delete()
            messages.success(request, "Item remove from watchlist!")

        else:
            messages.warning(request, "This item is not in watchlist!")

    return redirect("watchlist")

def closed_listings(request):
    listings = Listings.objects.filter(status="close")
    highest_bids = Bidding.objects.filter(item__in=listings).values('item').annotate(max_bid=Max('new_bidding'))     
    return render(request, "auctions/closed_listings.html", {
        "listings": listings,
        "highest_bids": highest_bids
    })
def closed_listings(request):
    listings = Listings.objects.filter(status="close")
    
    # Get highest bids per item
    highest_bids = Bidding.objects.filter(item__in=listings)\
        .values('item')\
        .annotate(max_bid=Max('new_bidding'))

    # Create a mapping: item_id -> max_bid
    highest_bid_map = {entry['item']: entry['max_bid'] for entry in highest_bids}
    
    # Create a set of listing IDs that the user won
    user_won = set()
    if request.user.is_authenticated:
        for listing in listings:
            max_bid = highest_bid_map.get(listing.id)
            if max_bid:
                winning_bid = Bidding.objects.filter(item=listing, new_bidding=max_bid).first()
                if winning_bid and winning_bid.user == request.user:
                    user_won.add(listing.id)

    return render(request, "auctions/closed_listings.html", {
        "listings": listings,
        "highest_bid_map": highest_bid_map,
        "user_won": user_won,
        "highest_bids": highest_bids
    })

# def biddings(request, id):
 
#     if not request.user.is_authenticated:
#         messages.error(request, "⚠️ Please login to auctions.")
#         return render(request, "auctions/login.html")
    
#     item = get_object_or_404(Listings, id=id)
#     highest_bid = Bidding.objects.filter(item=item).aggregate(Max('new_bidding'))['new_bidding__max'] or item.starting_bid
#     currentbid = highest_bid

#     highest_bid_obj = Bidding.objects.filter(item=item, new_bidding=highest_bid).first()
#     you_bid = "you bid is the current bid" if highest_bid_obj and highest_bid_obj.user == request.user else None

#     if request.method == 'POST':
#         form = Biding_form(request.POST)
#         if form.is_valid():
#             new_bid = form.cleaned_data['starting_bid']

#             if new_bid > item.starting_bid and new_bid > highest_bid:
#                 Bidding.objects.create(
#                     item=item,
#                     user=request.user,
#                     new_bidding=new_bid
#                 )
#                 return redirect("listings", id=id)
#             else:
#                 return render(request, "auctions/listings.html", {
#                     "form": form,
#                     "item": item,
#                     "username": request.user.username,
#                     "error": "⚠️ Bid must be higher than the current price!",
#                     "currentbid": currentbid,
#                     "you_bid": you_bid
#                 })
#     else:
#         form = Biding_form()

#     return render(request, "auctions/listings.html", {
#         "form": form,
#         "item": item,
#         "username": request.user.username,
#         "currentbid": currentbid,
#         "you_bid": you_bid
#     })

def biddings(request, id):
    if not request.user.is_authenticated:
        messages.error(request, "⚠️ Please login to auctions.")
        return render(request, "auctions/login.html")

    item = get_object_or_404(Listings, id=id)
    comments = Comment.objects.filter(listing=item).order_by('-timestamp')

    highest_bid = Bidding.objects.filter(item=item).aggregate(Max('new_bidding'))['new_bidding__max'] or item.starting_bid
    currentbid = highest_bid

    highest_bid_obj = Bidding.objects.filter(item=item, new_bidding=highest_bid).first()
    you_bid = "you bid is the current bid" if highest_bid_obj and highest_bid_obj.user == request.user else None

    form = Biding_form()
    comment_form = CommentForm()

    if request.method == 'POST':
        if 'submit_bid' in request.POST:
            form = Biding_form(request.POST)
            if form.is_valid():
                new_bid = form.cleaned_data['starting_bid']
                if new_bid > item.starting_bid and new_bid > highest_bid:
                    Bidding.objects.create(
                        item=item,
                        user=request.user,
                        new_bidding=new_bid
                    )
                    return redirect("listings", id=id)
                else:
                    return render(request, "auctions/listings.html", {
                        "form": form,
                        "comment_form": comment_form,
                        "comments": comments,
                        "item": item,
                        "username": request.user.username,
                        "error": "⚠️ Bid must be higher than the current price!",
                        "currentbid": currentbid,
                        "you_bid": you_bid
                    })

        elif 'submit_comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.listing = item
                comment.save()
                return redirect("listings", id=id)

    return render(request, "auctions/listings.html", {
        "form": form,
        "comment_form": comment_form,
        "comments": comments,
        "item": item,
        "username": request.user.username,
        "currentbid": currentbid,
        "you_bid": you_bid
    })

def category_filter(request, category_name):
    if category_name=="all":
        listings = Listings.objects.filter(status="ongoing")
    else:
        listings = Listings.objects.filter(category=category_name, status="ongoing")
    return render(request, "auctions/category_listings.html", {
        "category": category_name,
        "listings": listings
    })




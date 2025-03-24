from django.urls import path

from . import views

urlpatterns = [
    path("", views.active_list, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/<str:id>", views.listings, name="listings"),
    path("create_listings", views.create_listings, name="create_listings"),
    path("biding/<int:id>", views.biddings, name="biding"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/add/<int:item_id>/", views.add_to_watchlist, name="add_to_watchlist"),
    path("watchlist/remove/<int:item_id>/", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("closedlists", views.closed_listings, name="closed_listings"),
    path("categories/<str:category_name>/", views.category_filter, name="category_filter"),
]

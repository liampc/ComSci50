from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:product_id>", views.listings, name="listings"),
    path("listing/add_listing", views.add_listing, name="add_listing"),
    path("listing/categories", views.categories, name="categories"),
    path("listing/category/<str:category>", views.category, name="category"),
    path("watchlist/<str:user>", views.watchlist, name="watchlist"),
]

from django.urls import path

from . import views

app_name = 'ency'
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("newPage", views.newPage, name="newPage"),
    path("updatePage/<str:title>", views.updatePage, name="updatePage")
]

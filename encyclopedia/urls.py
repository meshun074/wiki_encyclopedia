from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("Search", views.searchEntry, name="search"),
    path("CreateEntry", views.createEntry, name="create"),
    path("RandomEntryPage", views.randomEntry, name="random"),
    path("EditEntry/<str:entryname>", views.editEntry, name="edit"),
    path("<str:entryname>", views.entrypage, name="getentrypage")
]

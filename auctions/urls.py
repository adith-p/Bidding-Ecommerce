from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("details/<int:list_id>", views.details, name="details"),
    path("search", views.search, name="search"),
    path("add_lists", views.add_lists, name="add_lists"),
    path("test", views.test, name="test"),
    path("bid/<int:list_id>", views.bid, name="bid")

]

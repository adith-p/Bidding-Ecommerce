from django.urls import path

from . import views

urlpatterns = [
    # Home
    path("", views.index, name="index"),
    # UserAuth
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),

    # Auction routes
    path("search", views.search, name="search"),
    path("add_lists", views.add_lists, name="add_lists"),
    path("details/<int:list_id>", views.details, name="details"),
    path("bid/<int:list_id>", views.bid, name="bid"),
    path("close/<int:list_id>", views.deactivate, name="close"),
    path("profile/mybids", views.mybids, name="mybids"),

    # Bookmarks
    path("profile/bookmarks", views.showBookmarks, name="bookmarks"),
    path("add-bookmark/<int:list_id>", views.addBookmark, name="addBookmark"),
    path("rm-bookmark/<int:list_id>", views.removeBookmark, name="rmBookmark"),



]

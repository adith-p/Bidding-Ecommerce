from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django import forms
from django.contrib import messages
from django.db.models import Q


from .models import User, Auction_list, Catagory, Bids, Bookmarks


class AddForm(forms.Form):
    title = forms.CharField(label="Title",
                            widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    desc = forms.CharField(widget=forms.Textarea(
        attrs={'cols': 80, 'rows': 10, 'placeholder': 'Description'}))
    image_url = forms.CharField(max_length=1000, label="Image Url", required=False,
                                widget=forms.TextInput(attrs={'placeholder': 'Image Url'}))
    bid = forms.FloatField(widget=forms.NumberInput(
        attrs={'placeholder': 'Enter Bid'}))


class BidForm(forms.Form):
    bid = forms.FloatField(widget=forms.NumberInput(
        attrs={'placeholder': 'Enter Bid'}))


def index(request):

    a_list = Auction_list.objects.filter(
        is_active=True).select_related("bid")
    catogory = Catagory.objects.all()

    return render(request, "auctions/index.html", {
        "a_list": a_list,
        "cat": catogory

    })


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
            messages.add_message(request, messages.WARNING,
                                 "Passwords must match.")
            return render(request, "auctions/register.html",)

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.add_message(request, messages.WARNING,
                                 "Username already taken.")
            return render(request, "auctions/register.html")
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def details(request, list_id):
    list_item = Auction_list.objects.get(pk=list_id)
    try:
        is_bookmarked = Bookmarks.objects.get(
            auction_id=list_id, bookmarks=request.user)
    except:
        content = {
            "list_item": list_item,
            "is_bookmarked": False

        }
    content = {
        "list_item": list_item,
        "is_bookmarked": True

    }

    return render(request, 'auctions/listing_page.html', content)


def search(request):
    if request.method == "POST":
        cat = request.POST.get("catagory")
        query = request.POST.get("search_query")
        c_list = Catagory.objects.all()

        if cat and cat != "Select Category":

            catagory = Catagory.objects.get(catagory_name=cat)
            cat_id = catagory.pk
            a_list = Auction_list.objects.filter(
                catagory=cat_id, is_active=True)

        else:
            a_list = Auction_list.objects.filter(is_active=True)
        if query:
            a_list = a_list.filter(
                Q(title__contains=query) | Q(desc__contains=query)
            )

        return render(request, "auctions/index.html", {
            "a_list": a_list,
            "cat": c_list

        })
    return HttpResponse("didt work")


def add_lists(request):
    catogory = Catagory.objects.all()
    if request.method == "POST":
        form = AddForm(request.POST)

        if form.is_valid():
            catagory_name = request.POST.get("catagory")
            print(request.POST.get("catagory"))
            if catagory_name != "Select Category":
                catagory_instance = Catagory.objects.get(
                    catagory_name=catagory_name)
            else:
                catagory_instance = None

            bid_instance = Bids(
                bid=form.cleaned_data["bid"], user=request.user)
            bid_instance.save()

            # if form.cleaned_data["image_url"] == '':
            #     form.cleaned_data["image_url"] = "images/placeholder.png"

            auction_item = Auction_list(
                title=form.cleaned_data["title"], desc=form.cleaned_data["desc"], image_url=form.cleaned_data["image_url"], bid=bid_instance, owner=request.user, catagory=catagory_instance,)

            auction_item.save()

            return redirect(reverse(details, args=[auction_item.pk]))

    return render(request, "auctions/add_lists.html", {
        "form": AddForm(),
        "cat": catogory
    })


def bid(request, list_id):
    list_item = get_object_or_404(Auction_list, pk=list_id)
    if request.method == "POST":
        user_bid = request.POST.get("number")

        bid_list = get_object_or_404(Bids, pk=list_item.bid.pk)

        if float(user_bid) > bid_list.bid:
            new_bid_item = Bids(
                bid=user_bid,
                user=request.user,
                auction_id=list_id
            )
            new_bid_item.save()
            list_item.bid = new_bid_item
            list_item.save()

            # bid_list.bid = user_bid
            # bid_list.user = request.user
            # bid_list.auction_id = list_id
            # bid_list.save()

            messages.add_message(request, messages.SUCCESS, "Bid Successful")
            return redirect(bid, list_id)
        else:
            messages.add_message(request, messages.INFO, "Bid Higher")
            return redirect(bid, list_id)

    return render(request, "auctions/listing_page.html", {
        "form": BidForm(),
        "list_item": list_item
    })


def profile(request):
    if request.user.is_authenticated:
        username = request.user.username
        user_object = User.objects.get(username=username)
        list_item = Auction_list.objects.filter(owner=user_object.pk)

    return render(request, "auctions/dashboard.html", {
        "list_items": list_item
    })


def deactivate(request, list_id):
    item_list = Auction_list.objects.get(pk=list_id)

    item_list.is_active = False
    item_list.save()

    return redirect(reverse("profile"))


def mybids(request):
    bid_list = Bids.objects.filter(auction_id__isnull=False, user=request.user)
    bid_data = []

    for bid in bid_list:
        auction_id = bid.auction_id
        try:
            auction_item = Auction_list.objects.get(pk=auction_id)
            bid_data.append({
                "id": bid.id,
                "title": auction_item.title,
                "bid": bid.bid,
                "auction_id": bid.auction_id,
                "bid_time": bid.bid_time,
            })
        except Auction_list.DoesNotExist:
            # Handle the case if an auction item does not exist
            pass

    return render(request, "auctions/your_bids.html", {
        "bid_data": bid_data,
    })


def showBookmarks(request):
    currentUser = request.user.pk
    bookmark = Bookmarks.objects.filter(bookmarks=currentUser)
    print(request.user)
    print(bookmark)
    print(bookmark[0].auction_id.title)

    return render(request, "auctions/bookmarks.html", {
        "bookmarks": bookmark
    })


def removeBookmark(request, list_id):
    # bookmark = Bookmarks.objects.get(
    #     auction_id=list_id, bookmarks=request.user)
    # bookmark.bookmarks.remove(bookmark)
    pass


def addBookmark(request, list_id):
    list_item = get_object_or_404(Auction_list, pk=list_id)

    currentUser = request.user.pk

    bookmark_new = Bookmarks.objects.create(auction_id=list_item)
    bookmark_new.bookmarks.add(currentUser)
    bookmark_new.save()
    return redirect(reverse(details, args=[list_id]))

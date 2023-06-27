from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from tinymce.widgets import TinyMCE


from .models import User, Auction_list, Catagory, Bids


class AddForm(forms.Form):
    title = forms.CharField(label="Title",
                            widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    desc = forms.CharField(widget=forms.Textarea(
        attrs={'cols': 80, 'rows': 10, 'placeholder': 'Description'}))
    image_url = forms.CharField(max_length=1000, label="Image Url",
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


def details(request, list_id):
    list_item = Auction_list.objects.get(pk=list_id)

    return render(request, 'auctions/listing_page.html', {
        "list_item": list_item
    })


def search(request):
    if request.method == "POST":
        cat = request.POST.get("catagory")
        c_list = Catagory.objects.all()
        print(cat)

        if cat and cat != "Select Category":

            catagory = Catagory.objects.get(catagory_name=cat)
            cat_id = catagory.pk

            a_list = Auction_list.objects.filter(
                catagory=cat_id, is_active=True)

        else:
            a_list = Auction_list.objects.filter(is_active=True)

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

            catagory_instance = Catagory.objects.get(
                catagory_name=request.POST.get("catagory"))

            bid_instance = Bids(
                bid=form.cleaned_data["bid"], user=request.user)
            bid_instance.save()

            auction_item = Auction_list(
                title=form.cleaned_data["title"], desc=form.cleaned_data["desc"], image_url=form.cleaned_data["image_url"], bid=bid_instance, owner=request.user, catagory=catagory_instance,)

            auction_item.save()

            return redirect(reverse(details, args=[auction_item.pk]))

    return render(request, "auctions/add_lists.html", {
        "form": AddForm(),
        "cat": catogory
    })


def test(request):
    return render(request, "auctions/list.html")


def bid(request, list_id):
    if request.method == "POST":
        form = BidForm(request.POST)
        print(list_id)
    return render(request, "auctions/listing_page.html", {
        "form": BidForm()
    })

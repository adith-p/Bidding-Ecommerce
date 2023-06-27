from django.contrib import admin
from .models import Auction_list, Catagory, Bids
# Register your models here.


class ListingAdmin(admin.ModelAdmin):
    list_display = ["title", "created_on",
                    "last_modified", "is_active", ]


class CatagoryAdmin(admin.ModelAdmin):
    list_display = ["catagory_name"]


admin.site.register(Auction_list, ListingAdmin)

admin.site.register(Catagory, CatagoryAdmin)

admin.site.register(Bids)

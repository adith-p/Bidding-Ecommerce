# Generated by Django 4.2.1 on 2023-08-11 06:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0032_auction_list_bookmarks_alter_auction_list_image_url"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="auction_list",
            name="bookmarks",
        ),
        migrations.CreateModel(
            name="Bookmarks",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "auction_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookmark",
                        to="auctions.auction_list",
                    ),
                ),
                (
                    "bookmarks",
                    models.ManyToManyField(
                        blank=True,
                        null=True,
                        related_name="bookmark_id",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]

# Generated by Django 4.2.1 on 2023-07-24 08:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0024_alter_auction_list_image_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="auction_list",
            name="image_url",
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]

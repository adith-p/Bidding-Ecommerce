# Generated by Django 4.2.1 on 2023-07-25 09:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0030_alter_auction_list_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="auction_list",
            name="title",
            field=models.CharField(max_length=30),
        ),
    ]
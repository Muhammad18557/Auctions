# Generated by Django 4.1.2 on 2022-12-25 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Auction",
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
                ("seller", models.CharField(default=None, max_length=64)),
                ("item", models.CharField(max_length=64)),
                ("description", models.TextField()),
                ("bid", models.IntegerField()),
                ("category", models.CharField(max_length=64)),
                ("posted_on", models.DateTimeField(auto_now_add=True)),
                ("image", models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name="Bid",
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
                ("item_id", models.IntegerField()),
                ("user", models.CharField(max_length=64)),
                ("item", models.CharField(max_length=64)),
                ("bid", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
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
                ("item_id", models.IntegerField()),
                ("user", models.CharField(max_length=64)),
                ("comment", models.TextField()),
                ("time", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Watchlist",
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
                ("user", models.CharField(max_length=64)),
                ("item_id", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Winner",
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
                ("owner", models.CharField(max_length=64)),
                ("winner", models.CharField(max_length=64)),
                ("item_id", models.IntegerField()),
                ("win_bid", models.IntegerField()),
                ("item", models.CharField(max_length=64)),
            ],
        ),
    ]

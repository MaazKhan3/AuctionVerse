# Generated by Django 5.0 on 2023-12-06 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_alter_user_first_name_purchasehistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='sold',
            field=models.BooleanField(default=False),
        ),
    ]

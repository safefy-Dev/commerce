# Generated by Django 5.1.6 on 2025-03-18 03:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_bidding_item_alter_watchlists_item_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidding',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.listings'),
        ),
        migrations.AlterField(
            model_name='bidding',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Bidding', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='watchlists',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.listings'),
        ),
        migrations.AlterField(
            model_name='watchlists',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlists', to=settings.AUTH_USER_MODEL),
        ),
    ]

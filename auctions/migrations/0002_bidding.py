# Generated by Django 5.1.6 on 2025-03-11 04:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bidding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_bidding', models.DecimalField(decimal_places=2, max_digits=10)),
                ('item', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='it1', to='auctions.listings')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings3', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

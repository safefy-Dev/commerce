# Generated by Django 5.1.6 on 2025-03-24 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='category',
            field=models.CharField(blank=True, choices=[('Fashion', 'Fashion'), ('Toys', 'Toys'), ('Electronics', 'Electronics'), ('Home', 'Home'), ('Other', 'Other')], max_length=50, null=True),
        ),
    ]

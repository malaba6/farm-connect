# Generated by Django 4.2.13 on 2024-05-27 19:49

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shoppingcarts', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ShoppingCarts',
            new_name='ShoppingCart',
        ),
    ]

# Generated by Django 4.2.13 on 2024-05-28 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_rename_image_product_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='farmer',
            field=models.IntegerField(),
        ),
    ]
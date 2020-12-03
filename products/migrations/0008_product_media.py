# Generated by Django 3.1 on 2020-12-03 00:05

from django.db import migrations, models
import products.storages


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20201202_2136'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='media',
            field=models.FileField(blank=True, null=True, storage=products.storages.ProtectedStorage(), upload_to='products/'),
        ),
    ]

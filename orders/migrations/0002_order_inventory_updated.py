# Generated by Django 3.1 on 2020-12-01 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='inventory_updated',
            field=models.BooleanField(default=False),
        ),
    ]

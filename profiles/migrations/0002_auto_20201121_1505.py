# Generated by Django 3.1 on 2020-11-21 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]

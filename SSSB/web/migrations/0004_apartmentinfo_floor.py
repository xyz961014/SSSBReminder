# Generated by Django 4.0.1 on 2024-08-13 20:02

from django.db import migrations
import web.models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_remove_apartmentinfo_floor'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartmentinfo',
            name='floor',
            field=web.models.FloorField(blank=True, default=None, null=True),
        ),
    ]
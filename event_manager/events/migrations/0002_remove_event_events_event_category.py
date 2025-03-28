# Generated by Django 5.1.7 on 2025-03-24 11:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="event",
            name="events",
        ),
        migrations.AddField(
            model_name="event",
            name="category",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="events",
                to="events.category",
            ),
            preserve_default=False,
        ),
    ]

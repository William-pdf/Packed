# Generated by Django 4.0.3 on 2022-08-01 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("packed_api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="packinglistitem",
            name="title",
            field=models.CharField(default=False, max_length=200),
        ),
    ]

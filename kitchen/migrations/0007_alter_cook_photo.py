# Generated by Django 4.2.3 on 2023-07-25 07:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("kitchen", "0006_dish_dish_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cook",
            name="photo",
            field=models.URLField(blank=True, null=True),
        ),
    ]

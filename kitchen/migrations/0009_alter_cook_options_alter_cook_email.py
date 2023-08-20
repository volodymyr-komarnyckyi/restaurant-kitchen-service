# Generated by Django 4.2.3 on 2023-08-12 20:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("kitchen", "0008_alter_dish_dish_photo"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="cook",
            options={"ordering": ["last_name"]},
        ),
        migrations.AlterField(
            model_name="cook",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
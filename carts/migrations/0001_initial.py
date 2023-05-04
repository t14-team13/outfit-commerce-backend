# Generated by Django 4.2 on 2023-05-04 19:15

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.IntegerField()),
                ("total_price", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                "ordering": ["id"],
            },
        ),
    ]

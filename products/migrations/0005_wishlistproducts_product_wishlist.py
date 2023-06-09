# Generated by Django 4.2 on 2023-05-09 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("wishlists", "0001_initial"),
        ("products", "0004_alter_product_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="WishListProducts",
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
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="products_wishlist",
                        to="products.product",
                    ),
                ),
                (
                    "wishlist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="wishlists_products",
                        to="wishlists.wishlist",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="product",
            name="wishlist",
            field=models.ManyToManyField(
                related_name="products_in_wishlist",
                through="products.WishListProducts",
                to="wishlists.wishlist",
            ),
        ),
    ]

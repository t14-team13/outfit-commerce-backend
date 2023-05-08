# Generated by Django 4.2 on 2023-05-04 19:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("products", "0001_initial"),
        ("carts", "0002_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products_added', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cartproducts',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current_cart', to='carts.cart'),
        ),
        migrations.AddField(
            model_name='cartproducts',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_products', to='products.product'),
        ),
    ]

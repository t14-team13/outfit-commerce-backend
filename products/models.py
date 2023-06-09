from django.db import models


class Product(models.Model):
    class Meta:
        ordering = ["id"]

    name = models.CharField(max_length=40)
    image = models.TextField(default=None, null=True)
    description = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    category = models.CharField(max_length=40)
    stock = models.IntegerField()
    sold = models.IntegerField(default=0)

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="products_added",
    )

    cart = models.ManyToManyField(
        "carts.Cart", related_name="products_in_cart", through="products.CartProducts"
    )

    wishlist = models.ManyToManyField(
        "wishlists.WishList",
        related_name="products_in_wishlist",
        through="products.WishListProducts",
    )


class CartProducts(models.Model):
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="cart_products",
    )

    cart = models.ForeignKey(
        "carts.Cart", on_delete=models.CASCADE, related_name="current_cart"
    )


class WishListProducts(models.Model):
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, related_name="products_wishlist"
    )

    wishlist = models.ForeignKey(
        "wishlists.WishList",
        on_delete=models.CASCADE,
        related_name="wishlists_products",
    )

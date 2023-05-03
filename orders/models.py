from django.db import models
import uuid

class OrderStatusChoices(models.TextChoices):
    ORDERS_PLACED = "Order placed"
    IN_PROGRESS = "Order in progress"
    DELIVERED = "Order delivered"
    NOT_INFORMED = "Not informed"

class Order(models.Model):

    status = models.CharField(
        max_length=50,
        choices = OrderStatusChoices.choices,
        default=OrderStatusChoices.NOT_INFORMED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(
        "users.User",
        on_delete= models.PROTECT,
        related_name="orders"
    )

    cart = models.ForeignKey(
        "carts.Cart",
        on_delete.PROTECT,
        related_name="cart_orders"
    )


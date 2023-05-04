from django.db import models

class OrderStatusChoices(models.TextChoices):
    ORDERS_PLACED = "Order placed"
    IN_PROGRESS = "Order in progress"
    DELIVERED = "Order delivered"

class Order(models.Model):

    status = models.CharField(
        max_length=50,
        choices = OrderStatusChoices.choices,
        default=OrderStatusChoices.ORDERS_PLACED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(
        "users.User",
        on_delete= models.PROTECT,
        related_name="orders"
    )

    products = models.ManyToManyField(
        "products.Product",
        related_name="orders"
    )
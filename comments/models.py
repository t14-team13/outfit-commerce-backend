from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Comment(models.Model):
    title = models.CharField(max_length=100)
    comment = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, related_name="product_comment"
    )

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="comment_user"
    )

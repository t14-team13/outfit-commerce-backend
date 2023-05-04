from django.db import models

# Create your models here.


class Cart(models.Model):
    class Meta:
        ordering = ["id"]

    amount = models.IntegerField()
    total_price = models.DecimalField(decimal_places=2, max_digits=10)
    user = models.OneToOneField("users.User", on_delete=models.CASCADE)

from django.db import models

# Create your models here.


class Cart(models.Model):
    class Meta:
        ordering = ["id"]

    # amount = models.IntegerField(default=0, blank=True, null=True)
    # total_price = models.DecimalField(
    #     decimal_places=2, max_digits=10, default=0, blank=True, null=True
    # )
    user = models.OneToOneField("users.User", on_delete=models.CASCADE)

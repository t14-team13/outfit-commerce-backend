from django.db import models

# Create your models here.


class Cart(models.Model):
    class Meta:
        ordering = "id"

    amount = models.IntegerField()
    total_price = models.DecimalField(decimal_places=2)
    user_id = models.OneToOneField("users.User", on_delete=models.CASCADE)

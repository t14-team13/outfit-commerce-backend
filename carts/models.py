from django.db import models

# Create your models here.


class Cart(models.Model):
    class Meta:
        ordering = ["id"]

    user = models.OneToOneField("users.User", on_delete=models.CASCADE)

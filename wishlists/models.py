from django.db import models

# Create your models here.


class WishList(models.Model):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE)

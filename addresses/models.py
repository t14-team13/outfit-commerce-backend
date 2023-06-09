from django.db import models


class Address(models.Model):
    street = models.CharField(max_length=150)
    city = models.CharField(max_length=40)
    state = models.CharField(max_length=40)
    number = models.CharField(max_length=40)
    complement = models.CharField(max_length=40, null=True, default=None)
    zipcode = models.CharField(max_length=40)

    selected = models.BooleanField(default=False)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="adress_user"
    )

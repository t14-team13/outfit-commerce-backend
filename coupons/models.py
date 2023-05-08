from django.db import models

# Create your models here.


class Coupon(models.Model):
    code = models.CharField(max_length=5)
    discount = models.IntegerField()
    amount = models.IntegerField()

    coupon_creator_user_admin = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="registered_coupons"
    )

    coupon_using_user = models.ManyToManyField(
        "carts.Cart", related_name="coupons_used"
    )

from django.db import models

# Create your models here.


class Coupon(models.Model):
    code = models.CharField(max_length=5)
    discount = models.IntegerField()
    amount = models.IntegerField()

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="registered_coupons"
    )

    coupon_using_cart = models.ManyToManyField(
        "carts.Cart", related_name="coupons_used", through="coupons.CouponPivot"
    )


class CouponPivot(models.Model):
    coupon = models.ForeignKey(
        "coupons.Coupon", on_delete=models.CASCADE, related_name="coupons"
    )

    cart = models.ForeignKey(
        "carts.Cart", on_delete=models.CASCADE, related_name="cart"
    )

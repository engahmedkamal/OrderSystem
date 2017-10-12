from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# Create your models here.
class Order(models.Model):
    restaurant_name = models.CharField(max_length=250)
    delivery_fees = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    menu_url = models.CharField(max_length=400)
    tax_percentage = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    total_price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, default='0')
    creator = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.restaurant_name


class OrderDetail(models.Model):
    item_name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    quantity = models.IntegerField(max_length=3, default=1)
    description = models.CharField(max_length=250, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return self.order_name
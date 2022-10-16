from django.db import models
from order.models import Order


# Create your models here.

class Payment(models.Model):
    order = models.ForeignKey(verbose_name='关联的订单', to=Order, on_delete=models.SET_NULL, blank=True, null=True)
    pay_id = models.CharField(verbose_name='支付的订单号', max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = '订单支付'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.pay_id







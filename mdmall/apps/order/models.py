from django.db import models
from user.models import User, Home


class OrderTemp(models.Model):
    user = models.ForeignKey(verbose_name='关联用户', to=User, on_delete=models.SET_NULL, blank=True, null=True)
    goods_id = models.IntegerField('商品id', blank=True, null=True)
    goods_name = models.CharField('商品名称', max_length=200, blank=True, null=True)
    goods_img = models.CharField('图片路径', max_length=500, blank=True, null=True)
    goods_count = models.IntegerField('商品数量', blank=True, null=True)
    goods_price = models.FloatField('商品价格', blank=True, null=True)
    total_price = models.FloatField('商品总价格', blank=True, null=True)
    goods_status = models.CharField('商品状态码', max_length=200, blank=True, null=True)
    category_id = models.IntegerField('商品类别', blank=True, null=True)
    specification = models.CharField('商品规格', max_length=200, blank=True, null=True)
    specification_id = models.IntegerField('商品规格id', blank=True, null=True)

    class Meta:
        db_table = 'md_order_temp'
        verbose_name = '订单临时存储'
        verbose_name_plural = verbose_name


class Order(models.Model):
    user = models.ForeignKey(verbose_name='关联用户', to=User, on_delete=models.SET_NULL, blank=True, null=True)
    home = models.ForeignKey(verbose_name='关联地址', to=Home, on_delete=models.SET_NULL, blank=True, null=True)
    order_id = models.CharField('订单id', max_length=200, blank=True, null=True)  # 生成
    create_time = models.DateTimeField('订单创建事件', auto_now_add=True, blank=True, null=True)  # 自动生成
    pay_method = models.CharField('支付方式', max_length=200, blank=True, null=True)
    price_count = models.FloatField('订单总价', blank=True, null=True)
    is_pay = models.BooleanField('是否支付', default=False)

    class Meta:
        db_table = 'md_order'
        verbose_name = '订单'
        verbose_name_plural = verbose_name


class OrderInfo(models.Model):
    user = models.ForeignKey(verbose_name='关联用户', to=User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(verbose_name='关联订单', to=Order, on_delete=models.SET_NULL, blank=True, null=True)
    goods_id = models.IntegerField('商品id', blank=True, null=True)
    goods_name = models.CharField('商品名称', max_length=200, blank=True, null=True)
    goods_img = models.CharField('图片路径', max_length=500, blank=True, null=True)
    goods_count = models.IntegerField('商品数量', blank=True, null=True)
    goods_price = models.FloatField('商品价格', blank=True, null=True)
    total_price = models.FloatField('商品总价格', blank=True, null=True)
    goods_status = models.CharField('商品状态码', max_length=200, blank=True, null=True)
    category_id = models.IntegerField('商品类别', blank=True, null=True)
    specification = models.CharField('商品规格', max_length=200, blank=True, null=True)
    specification_id = models.IntegerField('商品规格id', blank=True, null=True)

    class Meta:
        db_table = 'md_order_info'
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name

















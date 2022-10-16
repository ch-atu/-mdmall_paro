from django.db import models
from user.models import User


# Create your models here.
class MobileSpecification(models.Model):
    run_memory = models.CharField('运行内存', max_length=200, blank=True, null=True)
    storage = models.CharField('总存储空间', max_length=200, blank=True, null=True)
    color = models.CharField('颜色', max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'md_Mobile_Specification'
        verbose_name = '手机规格'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.run_memory}+{self.storage}+{self.color}'


class ComputerSpecification(models.Model):
    size = models.CharField('尺寸', max_length=200, blank=True, null=True)
    storage = models.CharField('总存储空间', max_length=200, blank=True, null=True)
    color = models.CharField('颜色', max_length=200, blank=True, null=True)
    run_memory = models.CharField('运行内存', max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'md_Computer_Specification'
        verbose_name = '电脑规格'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.size}+{self.run_memory}+{self.storage}+{self.color}'


class Category(models.Model):
    name = models.CharField('类别名称', max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'md_Category'
        verbose_name = '商品类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class MobileGoods(models.Model):
    name = models.CharField('商品名称', max_length=200, blank=True, null=True)
    price = models.FloatField('商品价格', blank=True, null=True)
    # image = models.ImageField('商品图片', upload_to='images/goods', default='')
    image = models.ImageField('商品图片', default='')
    stock = models.IntegerField('商品库存', blank=True, null=True)
    sales = models.IntegerField('商品销量', blank=True, null=True)
    account = models.CharField('商品描述', max_length=500, blank=True, null=True)
    detail = models.CharField('商品详情', max_length=500, blank=True, null=True)
    packing = models.CharField('规格与包装', max_length=500, blank=True, null=True)
    service = models.CharField('售后服务', max_length=500, blank=True, null=True)
    specification_1 = models.ForeignKey(verbose_name='商品规格1', to=MobileSpecification, related_name='spec_1',
                                        on_delete=models.SET_NULL,
                                        blank=True, null=True)
    specification_2 = models.ForeignKey(verbose_name='商品规格2', to=MobileSpecification, related_name='spec_2',
                                        on_delete=models.SET_NULL,
                                        blank=True, null=True)
    specification_3 = models.ForeignKey(verbose_name='商品规格3', to=MobileSpecification, related_name='spec_3',
                                        on_delete=models.SET_NULL,
                                        blank=True, null=True)
    category = models.ForeignKey(verbose_name='商品类别', to=Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'md_Mobile_Goods'
        verbose_name = '手机商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ComputerGoods(models.Model):
    name = models.CharField('商品名称', max_length=200, blank=True, null=True)
    price = models.FloatField('商品价格', blank=True, null=True)
    # image = models.ImageField('商品图片', upload_to='images/goods', default='')
    image = models.ImageField('商品图片', default='')
    stock = models.IntegerField('商品库存', blank=True, null=True)
    sales = models.IntegerField('商品销量', blank=True, null=True)
    account = models.CharField('商品描述', max_length=500, blank=True, null=True)
    detail = models.CharField('商品详情', max_length=500, blank=True, null=True)
    packing = models.CharField('规格与包装', max_length=500, blank=True, null=True)
    service = models.CharField('售后服务', max_length=500, blank=True, null=True)
    specification_1 = models.ForeignKey(verbose_name='商品规格1', to=ComputerSpecification, related_name='spec_1',
                                        on_delete=models.SET_NULL,
                                        blank=True, null=True)
    specification_2 = models.ForeignKey(verbose_name='商品规格2', to=ComputerSpecification, related_name='spec_2',
                                        on_delete=models.SET_NULL,
                                        blank=True, null=True)
    specification_3 = models.ForeignKey(verbose_name='商品规格3', to=ComputerSpecification, related_name='spec_3',
                                        on_delete=models.SET_NULL,
                                        blank=True, null=True)
    category = models.ForeignKey(verbose_name='商品类别', to=Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'md_Computer_Goods'
        verbose_name = '电脑商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Estimate(models.Model):
    mobile = models.ForeignKey(verbose_name='手机', to=MobileGoods, on_delete=models.SET_NULL, blank=True, null=True)
    computer = models.ForeignKey(verbose_name='电脑', to=ComputerGoods, on_delete=models.SET_NULL, blank=True, null=True)
    describe = models.CharField('评价内容', max_length=500, blank=True, null=True)
    score = models.FloatField('评分', blank=True, null=True)
    user = models.ForeignKey(verbose_name='用户', to=User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'md_Estimate'
        verbose_name = '商品评价'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username

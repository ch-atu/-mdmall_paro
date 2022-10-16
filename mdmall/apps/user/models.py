from .utils import validate_username

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(
        '用户名',
        max_length=150,
        unique=True,
        validators=[validate_username],
        error_messages={
            'unique': '用户名只能是唯一的',
        },
    )
    mobile = models.CharField('手机号', blank=True, null=True, unique=True, max_length=11, )
    email_active = models.BooleanField('邮箱是否激活', default=False)

    class Meta:
        db_table = 'User'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class Home(models.Model):
    user = models.ForeignKey(verbose_name='用户', to=User, on_delete=models.SET_NULL, blank=True, null=True)
    receive = models.CharField(verbose_name='收货人', max_length=100, blank=True, null=True)
    area = models.CharField(verbose_name='所在地区', max_length=200, blank=True, null=True)
    address = models.CharField(verbose_name='地址', max_length=200, blank=True, null=True)
    mobile = models.CharField(verbose_name='联系电话', max_length=200, blank=True, null=True)
    email = models.CharField(verbose_name='邮箱', max_length=200, blank=True, null=True)
    is_default = models.BooleanField(verbose_name='是否默认', default=False)

    class Meta:
        db_table = "user_home"
        verbose_name = "收货地址"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address

# Generated by Django 3.2 on 2022-05-19 14:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='类别名称')),
            ],
            options={
                'verbose_name': '商品类别',
                'verbose_name_plural': '商品类别',
                'db_table': 'Category',
            },
        ),
        migrations.CreateModel(
            name='ComputerSpecification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(blank=True, max_length=200, null=True, verbose_name='大小')),
                ('storage', models.CharField(blank=True, max_length=200, null=True, verbose_name='总存储空间')),
                ('color', models.CharField(blank=True, max_length=200, null=True, verbose_name='颜色')),
                ('run_memory', models.CharField(blank=True, max_length=200, null=True, verbose_name='运行内存')),
            ],
            options={
                'verbose_name': '电脑规格',
                'verbose_name_plural': '电脑规格',
                'db_table': 'Computer_Specification',
            },
        ),
        migrations.CreateModel(
            name='Estimate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('describe', models.CharField(blank=True, max_length=500, null=True, verbose_name='评价内容')),
                ('score', models.FloatField(blank=True, null=True, verbose_name='评分')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '商品评价',
                'verbose_name_plural': '商品评价',
                'db_table': 'Estimate',
            },
        ),
        migrations.CreateModel(
            name='MobileSpecification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('run_memory', models.CharField(blank=True, max_length=200, null=True, verbose_name='运行内存')),
                ('storage', models.CharField(blank=True, max_length=200, null=True, verbose_name='总存储空间')),
                ('color', models.CharField(blank=True, max_length=200, null=True, verbose_name='颜色')),
            ],
            options={
                'verbose_name': '手机规格',
                'verbose_name_plural': '手机规格',
                'db_table': 'Mobile_Specification',
            },
        ),
        migrations.CreateModel(
            name='MobileGoods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='商品名称')),
                ('price', models.FloatField(blank=True, null=True, verbose_name='商品价格')),
                ('image', models.ImageField(default='', upload_to='images/goods', verbose_name='商品图片')),
                ('stock', models.IntegerField(blank=True, null=True, verbose_name='商品库存')),
                ('sales', models.IntegerField(blank=True, null=True, verbose_name='商品销量')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.category', verbose_name='商品类别')),
                ('estimate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.estimate', verbose_name='商品评价')),
                ('specification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.mobilespecification', verbose_name='商品规格')),
            ],
            options={
                'verbose_name': '手机商品',
                'verbose_name_plural': '手机商品',
                'db_table': 'Mobile_Goods',
            },
        ),
        migrations.CreateModel(
            name='ComputerGoods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='商品名称')),
                ('price', models.FloatField(blank=True, null=True, verbose_name='商品价格')),
                ('image', models.ImageField(default='', upload_to='images/goods', verbose_name='商品图片')),
                ('stock', models.IntegerField(blank=True, null=True, verbose_name='商品库存')),
                ('sales', models.IntegerField(blank=True, null=True, verbose_name='商品销量')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.category', verbose_name='商品类别')),
                ('estimate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.estimate', verbose_name='商品评价')),
                ('specification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.computerspecification', verbose_name='商品规格')),
            ],
            options={
                'verbose_name': '手机商品',
                'verbose_name_plural': '手机商品',
                'db_table': 'Computer_Goods',
            },
        ),
    ]

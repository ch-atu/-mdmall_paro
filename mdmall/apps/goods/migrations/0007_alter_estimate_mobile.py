# Generated by Django 3.2 on 2022-05-19 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0006_auto_20220519_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estimate',
            name='mobile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='goods.mobilegoods', verbose_name='手机'),
        ),
    ]

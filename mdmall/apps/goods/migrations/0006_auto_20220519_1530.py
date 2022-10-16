# Generated by Django 3.2 on 2022-05-19 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0005_auto_20220519_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computergoods',
            name='specification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='goods.computerspecification', verbose_name='商品规格'),
        ),
        migrations.AlterField(
            model_name='mobilegoods',
            name='specification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='goods.mobilespecification', verbose_name='商品规格'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-08-02 08:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_auto_20190802_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='pay_status',
            field=models.CharField(choices=[('TRADE_FINISHED', '交易结束'), ('TRADE_CLOSE', '交易关闭'), ('TRADE_SUCCESS', '成功'), ('WAIT_BUYER_PAY', '交易创建'), ('paying', '待支付')], default='paying', max_length=20, verbose_name='交易状态'),
        ),
        migrations.AlterModelTable(
            name='ordergoods',
            table=None,
        ),
        migrations.AlterModelTable(
            name='orderinfo',
            table=None,
        ),
    ]

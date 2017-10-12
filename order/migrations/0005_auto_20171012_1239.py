# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_auto_20171012_1125'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='creator_user',
            new_name='creator',
        ),
        migrations.RenameField(
            model_name='orderdetail',
            old_name='order_name',
            new_name='item_name',
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_fees',
            field=models.DecimalField(null=True, max_digits=5, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default=b'0', max_length=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='tax_percentage',
            field=models.DecimalField(null=True, max_digits=3, decimal_places=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(null=True, max_digits=7, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='description',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='price',
            field=models.DecimalField(null=True, max_digits=6, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='quantity',
            field=models.IntegerField(default=1, max_length=3),
        ),
    ]

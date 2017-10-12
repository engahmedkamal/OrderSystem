# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('restaurant_name', models.CharField(max_length=250)),
                ('delivery_fees', models.DecimalField(max_digits=5, decimal_places=2)),
                ('menu_url', models.CharField(max_length=400)),
                ('tax_percentage', models.DecimalField(max_digits=3, decimal_places=1)),
                ('total_price', models.DecimalField(max_digits=7, decimal_places=2)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=1)),
                ('creator_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order_details',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_name', models.CharField(max_length=250)),
                ('price', models.DecimalField(max_digits=6, decimal_places=2)),
                ('count', models.IntegerField(max_length=3)),
                ('description', models.CharField(max_length=250)),
                ('order_id', models.ForeignKey(to='order.Order')),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

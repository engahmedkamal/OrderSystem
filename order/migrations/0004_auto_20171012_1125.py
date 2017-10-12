# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20171012_1049'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='creator_id',
            new_name='creator_user',
        ),
        migrations.RenameField(
            model_name='orderdetail',
            old_name='order_id',
            new_name='order',
        ),
        migrations.RenameField(
            model_name='orderdetail',
            old_name='user_id',
            new_name='user',
        ),
    ]

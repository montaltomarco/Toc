# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('toc', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itineraire',
            old_name='type_voiture',
            new_name='type_transport',
        ),
    ]

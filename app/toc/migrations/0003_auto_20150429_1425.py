# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('toc', '0002_auto_20150428_1255'),
    ]

    operations = [
        migrations.CreateModel(
            name='Data_velo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField()),
                ('contract_name', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('banking', models.BooleanField(verbose_name=b'banking')),
                ('bonus', models.BooleanField(verbose_name=b'bonus')),
                ('status', models.CharField(max_length=200)),
                ('bike_stands', models.IntegerField()),
                ('available_bike_stands', models.IntegerField()),
                ('available_bikes', models.IntegerField()),
                ('last_update', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Lieu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lat', models.FloatField(verbose_name=b'Latitude')),
                ('lon', models.FloatField(verbose_name=b'Longitude')),
                ('adresse', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Personne',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=200)),
                ('prenom', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('mot_de_pass', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Portion_de_route',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type_transport', models.CharField(max_length=200)),
                ('en_cours', models.BooleanField(verbose_name=b'en_cours')),
                ('consomation_co2', models.FloatField(verbose_name=b'CO2')),
                ('taux_pollution', models.FloatField(verbose_name=b'Pollution')),
            ],
        ),
        migrations.CreateModel(
            name='Profil',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type_personne', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='itineraire',
            name='pub_date',
        ),
        migrations.RemoveField(
            model_name='itineraire',
            name='type_transport',
        ),
        migrations.AddField(
            model_name='data_velo',
            name='position',
            field=models.ForeignKey(to='toc.Lieu'),
        ),
        migrations.AddField(
            model_name='itineraire',
            name='end_pos',
            field=models.ForeignKey(related_name='end_pos', default=0, to='toc.Lieu'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='itineraire',
            name='persones',
            field=models.ManyToManyField(to='toc.Personne'),
        ),
        migrations.AddField(
            model_name='itineraire',
            name='portion',
            field=models.ManyToManyField(to='toc.Portion_de_route'),
        ),
        migrations.AddField(
            model_name='itineraire',
            name='start_pos',
            field=models.ForeignKey(related_name='start_pos', default=0, to='toc.Lieu'),
            preserve_default=False,
        ),
    ]

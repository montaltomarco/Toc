# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Data_meteo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamps', models.IntegerField()),
                ('pluie', models.FloatField()),
                ('pluie_convective', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Data_velo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField()),
                ('contract_name', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('adresse', models.CharField(max_length=200)),
                ('banking', models.BooleanField(verbose_name=b'banking')),
                ('bonus', models.BooleanField(verbose_name=b'bonus')),
                ('status', models.CharField(max_length=200)),
                ('bike_stands', models.IntegerField()),
                ('available_bike_stands', models.IntegerField()),
                ('available_bikes', models.IntegerField()),
                ('last_update', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DistanceInterStation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('distance', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Itineraire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('duree', models.FloatField()),
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
            name='Ligne_TCL',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codeTitan', models.CharField(max_length=20)),
                ('ligne', models.CharField(max_length=20)),
                ('sens', models.CharField(max_length=20)),
                ('indice', models.CharField(max_length=100)),
                ('infos', models.CharField(max_length=100)),
                ('libelle', models.CharField(max_length=20)),
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
                ('vitesse_pied', models.FloatField(default=1.0)),
                ('vitesse_velo', models.FloatField(default=5.0)),
                ('temps_start', models.IntegerField(default=100)),
                ('temps_stop', models.IntegerField(default=100)),
            ],
        ),
        migrations.CreateModel(
            name='Profil',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type_personne', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('moyen_transport', models.CharField(max_length=30)),
                ('en_cours', models.BooleanField(verbose_name=b'en_cours')),
                ('temps', models.IntegerField()),
                ('taux_pollution', models.FloatField(verbose_name=b'Pollution')),
            ],
        ),
        migrations.CreateModel(
            name='Trajet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('distance_directe', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Vecteur',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('distance', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Arret_TCL',
            fields=[
                ('lieu_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='toc.Lieu')),
                ('id_station', models.IntegerField()),
                ('nom', models.CharField(max_length=100)),
                ('pmr', models.BooleanField()),
                ('escalator', models.BooleanField()),
            ],
            bases=('toc.lieu',),
        ),
        migrations.CreateModel(
            name='Borne_velo',
            fields=[
                ('lieu_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='toc.Lieu')),
                ('nbarceaux', models.IntegerField()),
            ],
            bases=('toc.lieu',),
        ),
        migrations.CreateModel(
            name='Station_autopartage',
            fields=[
                ('lieu_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='toc.Lieu')),
                ('nom', models.CharField(max_length=200)),
                ('identifiantstation', models.CharField(max_length=200)),
                ('commune', models.CharField(max_length=200)),
                ('typeautopartage', models.CharField(max_length=200)),
            ],
            bases=('toc.lieu',),
        ),
        migrations.CreateModel(
            name='Station_velov',
            fields=[
                ('lieu_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='toc.Lieu')),
                ('number_station', models.IntegerField()),
                ('nb_velos', models.IntegerField()),
                ('nb_places', models.IntegerField()),
            ],
            bases=('toc.lieu',),
        ),
        migrations.AddField(
            model_name='vecteur',
            name='arrivee',
            field=models.ManyToManyField(related_name='arrivee', to='toc.Lieu'),
        ),
        migrations.AddField(
            model_name='vecteur',
            name='depart',
            field=models.ManyToManyField(related_name='depart', to='toc.Lieu'),
        ),
        migrations.AddField(
            model_name='trajet',
            name='end_pos',
            field=models.ForeignKey(related_name='end_trajet_pos', to='toc.Lieu'),
        ),
        migrations.AddField(
            model_name='trajet',
            name='start_pos',
            field=models.ForeignKey(related_name='start_trajet_pos', to='toc.Lieu'),
        ),
        migrations.AddField(
            model_name='section',
            name='trajet',
            field=models.ForeignKey(to='toc.Trajet'),
        ),
        migrations.AddField(
            model_name='itineraire',
            name='end_pos',
            field=models.ForeignKey(related_name='end_pos', to='toc.Lieu'),
        ),
        migrations.AddField(
            model_name='itineraire',
            name='personnes',
            field=models.ManyToManyField(to='toc.Personne'),
        ),
        migrations.AddField(
            model_name='itineraire',
            name='sections',
            field=models.ManyToManyField(to='toc.Section'),
        ),
        migrations.AddField(
            model_name='itineraire',
            name='start_pos',
            field=models.ForeignKey(related_name='start_pos', to='toc.Lieu'),
        ),
        migrations.AddField(
            model_name='ligne_tcl',
            name='arrets',
            field=models.ManyToManyField(to='toc.Arret_TCL'),
        ),
        migrations.AddField(
            model_name='ligne_tcl',
            name='stations_velov',
            field=models.ManyToManyField(to='toc.Station_velov'),
        ),
        migrations.AddField(
            model_name='distanceinterstation',
            name='stationArrivee',
            field=models.ForeignKey(related_name='stationArrivee', to='toc.Station_velov'),
        ),
        migrations.AddField(
            model_name='distanceinterstation',
            name='stationDepart',
            field=models.ForeignKey(related_name='stationDepart', to='toc.Station_velov'),
        ),
        migrations.AddField(
            model_name='arret_tcl',
            name='stations_velov_proches',
            field=models.ManyToManyField(to='toc.Station_velov'),
        ),
    ]

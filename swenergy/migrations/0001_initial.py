# Generated by Django 4.1 on 2022-09-04 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p', models.FloatField()),
                ('q', models.FloatField()),
                ('s', models.FloatField()),
                ('urms', models.FloatField()),
                ('itrms', models.FloatField()),
                ('pf', models.FloatField()),
                ('pg', models.FloatField()),
                ('ep', models.FloatField()),
                ('eq', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('time', models.TimeField()),
                ('pt', models.FloatField()),
                ('qt', models.FloatField()),
                ('st', models.FloatField()),
                ('itrms', models.FloatField()),
                ('pft', models.FloatField()),
                ('freq', models.FloatField()),
                ('ept', models.FloatField()),
                ('eqt', models.FloatField()),
                ('yuaub', models.FloatField()),
                ('yuauc', models.FloatField()),
                ('yubuc', models.FloatField()),
                ('tpsd', models.FloatField()),
            ],
        ),
    ]

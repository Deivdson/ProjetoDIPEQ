# Generated by Django 4.1 on 2022-09-05 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swenergy', '0002_fase_sensor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consumo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField()),
                ('inicio', models.FloatField()),
                ('fim', models.FloatField()),
                ('total', models.FloatField()),
            ],
        ),
    ]
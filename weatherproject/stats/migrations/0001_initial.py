# Generated by Django 4.2 on 2023-05-03 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station_code', models.CharField(max_length=11)),
                ('recorded_on', models.DateField()),
                ('max_temperature', models.DecimalField(decimal_places=1, max_digits=3, null=True)),
                ('min_temperature', models.DecimalField(decimal_places=1, max_digits=3, null=True)),
                ('precipitation', models.DecimalField(decimal_places=1, max_digits=4, null=True)),
            ],
            options={
                'unique_together': {('station_code', 'recorded_on')},
            },
        ),
    ]

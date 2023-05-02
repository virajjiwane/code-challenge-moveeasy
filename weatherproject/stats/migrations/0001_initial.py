# Generated by Django 4.2 on 2023-05-02 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalRecords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station_code', models.CharField(max_length=11)),
                ('recorded_on', models.DateField()),
                ('max_temperature', models.DecimalField(decimal_places=1, max_digits=3)),
                ('min_temperature', models.DecimalField(decimal_places=1, max_digits=3)),
                ('precipitation', models.DecimalField(decimal_places=1, max_digits=4)),
            ],
            options={
                'unique_together': {('station_code', 'recorded_on')},
            },
        ),
    ]

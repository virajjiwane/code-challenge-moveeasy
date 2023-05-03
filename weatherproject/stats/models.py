from django.db import models


# Create your models here.


class HistoricalRecord(models.Model):
    station_code = models.CharField(max_length=11)
    recorded_on = models.DateField()
    # Since data is in tenths, having decimal places to 1 and assuming max temperature wont reach 100,
    # keeping max_digits as 3
    max_temperature = models.DecimalField(decimal_places=1, max_digits=3, null=True)
    min_temperature = models.DecimalField(decimal_places=1, max_digits=3, null=True)
    precipitation = models.DecimalField(decimal_places=1, max_digits=4, null=True)

    class Meta:
        unique_together = ('station_code', 'recorded_on')


class Statistic(models.Model):
    station_code = models.CharField(max_length=11)
    year = models.PositiveSmallIntegerField()
    avg_max_temperature = models.DecimalField(decimal_places=1, max_digits=3, null=True)
    avg_min_temperature = models.DecimalField(decimal_places=1, max_digits=3, null=True)
    total_precipitation = models.DecimalField(decimal_places=1, max_digits=5, null=True)

    class Meta:
        unique_together = ('station_code', 'year')

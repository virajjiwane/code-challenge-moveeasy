from django.db import models

# Create your models here.


class HistoricalRecord(models.Model):
    station_code = models.CharField(max_length=11)
    recorded_on = models.DateField()
    # Since data is in tenths, having decimal places to 1 and assuming max temperature wont reach 100,
    # keeping max_digits as 3
    max_temperature = models.DecimalField(decimal_places=1, max_digits=3)
    min_temperature = models.DecimalField(decimal_places=1, max_digits=3)
    precipitation = models.DecimalField(decimal_places=1, max_digits=4)

    class Meta:
        unique_together = ('station_code', 'recorded_on')

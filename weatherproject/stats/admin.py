from django.contrib import admin

# Register your models here.
from weatherproject.stats.models import HistoricalRecords

admin.site.register(HistoricalRecords)

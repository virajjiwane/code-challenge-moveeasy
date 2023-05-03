from django.contrib import admin

# Register your models here.
from .models import HistoricalRecord, Statistic

admin.site.register(HistoricalRecord)
admin.site.register(Statistic)

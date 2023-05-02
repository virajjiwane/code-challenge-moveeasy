from django.contrib import admin

# Register your models here.
from .models import HistoricalRecord

admin.site.register(HistoricalRecord)

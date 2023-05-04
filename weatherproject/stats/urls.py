from django.urls import path

from .views import HistoricalRecordView, StatisticView

urlpatterns = [
    path('', HistoricalRecordView.as_view(), name='historical_record'),
    path('stats', StatisticView.as_view(), name='statistic')
]

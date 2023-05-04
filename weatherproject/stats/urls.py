from django.urls import path

from .views import HistoricalRecordView, StatisticView

urlpatterns = [
    path('', HistoricalRecordView.as_view()),
    path('stats', StatisticView.as_view())
]

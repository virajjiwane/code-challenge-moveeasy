# Create your views here.
import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions

from .models import HistoricalRecord, Statistic
from .serializers import HistoricalRecordSerializer, StatisticSerializer

logger = logging.getLogger('django')

from drf_yasg import openapi

year_param = openapi.Parameter('year', openapi.IN_QUERY, description="Year", type=openapi.TYPE_INTEGER, )
station_code_param = openapi.Parameter('station_code', openapi.IN_QUERY, description="Station Code",
                                       type=openapi.TYPE_STRING, )


class HistoricalRecordView(generics.ListAPIView):
    model = HistoricalRecord
    serializer_class = HistoricalRecordSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = HistoricalRecord.objects.all()
        station_code = self.request.GET.get('station_code', None)
        year = self.request.GET.get('year', None)
        if year is not None:
            queryset = queryset.filter(recorded_on__year=year)
        if station_code is not None:
            queryset = queryset.filter(station_code=station_code)
        return queryset


class StatisticView(generics.ListAPIView):
    model = Statistic
    serializer_class = StatisticSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @swagger_auto_schema(manual_parameters=[year_param, station_code_param])
    def get_queryset(self):
        queryset = Statistic.objects.all()
        station_code = self.request.GET.get('station_code', None)
        year = self.request.GET.get('year', None)
        if year is not None:
            queryset = queryset.filter(year=year)
        if station_code is not None:
            queryset = queryset.filter(station_code=station_code)
        return queryset

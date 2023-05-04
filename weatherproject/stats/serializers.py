from rest_framework import serializers

from .models import HistoricalRecord, Statistic


class HistoricalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalRecord
        exclude = ('id',)


class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        exclude = ('id',)

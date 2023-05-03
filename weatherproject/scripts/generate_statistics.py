"""
This module contains functions to calculate statistics over the DB and populate the statistic DB.
"""
import operator
from functools import reduce

from django.db.models import F, Avg, Q, Sum
from stats.models import HistoricalRecord, Statistic
import logging
logger = logging.getLogger('django')


def run():
    """
    This function is the entry point of generating stats. It will get called before django startup.
    It also tackles duplicate values or program-reruns.
    """
    logger.info("Generating statistics")
    existing_stats = Statistic.objects.values('year', 'station_code')
    if existing_stats:
        query = reduce(operator.or_, map(lambda es: Q(year=es['year'], station_code=es['station_code']), existing_stats))
    else:
        query = Q()
    statistics = HistoricalRecord.objects\
        .annotate(year=F('recorded_on__year'))\
        .values('year', 'station_code')\
        .exclude(query)\
        .annotate(avg_max_temperature=Avg('max_temperature', filter=Q(max_temperature__isnull=False)),
                  avg_min_temperature=Avg('min_temperature', filter=Q(min_temperature__isnull=False)),
                  total_precipitation=Sum('precipitation'))

    statistic_obj_list = map(lambda s: Statistic(**s), statistics)
    statistic_obj_list = Statistic.objects.bulk_create(statistic_obj_list)
    logger.info(f"{len(statistic_obj_list)} stats inserted")
    logger.info("Generated statistics")

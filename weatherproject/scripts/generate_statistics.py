"""
This module contains functions to calculate statistics over the DB and populate the statistic DB.
"""
import logging
import traceback
from multiprocessing import cpu_count, Pool

from django.db.models import F, Avg, Q, Sum, Count
from stats.models import HistoricalRecord, Statistic

logger = logging.getLogger('django')


def generate_stats(station_code):
    """
    This function generates and inserts stats into DB if not already present.
    :param station_code:
    :return: Count of records inserted. Default is 0
    """

    inserted_record_count = 0
    try:
        years = Statistic.objects \
            .filter(station_code=station_code) \
            .values('year') \
            .annotate(Count('year')) \
            .values_list('year', flat=True)
        statistics = HistoricalRecord.objects \
            .filter(station_code=station_code) \
            .annotate(year=F('recorded_on__year')) \
            .values('year', 'station_code') \
            .exclude(year__in=years) \
            .annotate(avg_max_temperature=Avg('max_temperature', filter=Q(max_temperature__isnull=False)),
                      avg_min_temperature=Avg('min_temperature', filter=Q(min_temperature__isnull=False)),
                      total_precipitation=Sum('precipitation'))

        statistic_obj_list = map(lambda s: Statistic(**s), statistics)
        statistic_obj_list = Statistic.objects.bulk_create(statistic_obj_list)
        inserted_record_count = len(statistic_obj_list)
    except:
        logger.error(f"Error processing {station_code}")
        traceback.print_exc()

    return inserted_record_count


def run():
    """
    This function is the entry point of generating stats. It will get called before django startup.
    It also tackles duplicate values or program-reruns.
    """
    logger.info("Generating statistics")
    stations = HistoricalRecord.objects.values('station_code').annotate(Count('station_code')).values_list(
        'station_code', flat=True)
    logger.info(f'Using {cpu_count()} processes in parallel')
    pool = Pool(cpu_count())
    inserted_records_count = sum(pool.map(generate_stats, stations))

    logger.info(f"{inserted_records_count} stats inserted")
    logger.info("Generated statistics")

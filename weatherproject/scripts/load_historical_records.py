"""
This module contains functions to load data in DB.
"""

import logging
import os
import time
import traceback
from datetime import datetime
from decimal import Decimal
from multiprocessing import cpu_count, Pool
from os.path import isfile, join

from stats.models import HistoricalRecord

logger = logging.getLogger('django')


def clean(max_temperature, min_temperature, precipitation, recorded_on):
    recorded_on = datetime.strptime(recorded_on, '%Y%m%d')
    max_temperature = Decimal(max_temperature)
    min_temperature = Decimal(min_temperature)
    precipitation = Decimal(precipitation)

    # Check nulls
    null_value = -9999
    if max_temperature == null_value:
        max_temperature = None
    else:
        max_temperature /= 10

    if min_temperature == null_value:
        min_temperature = None
    else:
        min_temperature /= 10

    if precipitation == null_value:
        precipitation = None
    else:
        precipitation /= 10

    return max_temperature, min_temperature, precipitation, recorded_on


def process_file(file_path) -> int:
    """
    This function inserts record into DB is not already present.
    This function uses memory efficient way of iterating over file and using bulk insert operation to write into
    database while ignoring the duplicates.
    :param file_path:
    :return: Count of records inserted. Default is 0
    """

    inserted_record_count = 0
    try:
        full_name = os.path.basename(file_path)
        station_code = os.path.splitext(full_name)[0]

        existing_dates = map(lambda date: date.strftime('%Y%m%d'),
                             HistoricalRecord.objects \
                             .filter(station_code=station_code) \
                             .values_list('recorded_on', flat=True))

        record_list = []
        with open(file_path) as txt_file:
            for line in txt_file:
                recorded_on, max_temperature, min_temperature, precipitation = line.split()
                # Checking for duplicates
                if recorded_on in existing_dates:
                    continue
                max_temperature, min_temperature, precipitation, recorded_on = \
                    clean(max_temperature, min_temperature, precipitation, recorded_on)

                record_list.append(HistoricalRecord(
                    station_code=station_code,
                    recorded_on=recorded_on,
                    max_temperature=max_temperature,
                    min_temperature=min_temperature,
                    precipitation=precipitation
                ))
                inserted_record_count += 1

        if record_list:
            HistoricalRecord.objects.bulk_create(record_list)

    except:
        logger.error(f"Error processing {file_path}")
        traceback.print_exc()
    return inserted_record_count


def run():
    """
    This function is the entry point of populating data. It will get called before django startup.
    This function is responsible for creating parallel processes for inserting data. And log loading start and end time
    and inserted records count.
    """

    start_time = time.time()
    logger.info('Loading Records Started')

    data_dir = os.environ.get('DATA_DIR')
    logger.info(f'Reading {data_dir} Directory')

    files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if isfile(join(data_dir, f))]
    logger.info(f'Found {len(files)} Files')

    logger.info(f'Using {cpu_count()} processes in parallel')
    pool = Pool(cpu_count())
    inserted_records_count = sum(pool.map(process_file, files))

    if inserted_records_count > 0:
        logger.info(f'{inserted_records_count} records inserted in {time.time() - start_time} seconds')
    else:
        logger.info(f'{inserted_records_count} records inserted')

    logger.info('Loading Records Finished')

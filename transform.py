"""
transform.py
"""

import dateutil.parser


def transform_sleep_data(data):
    for row in data:
        # map the hypnogram data to a more readable format
        # 'D' = deep sleep
        # 'L' = light sleep
        # 'R' = REM sleep
        # 'A' = awake
        row['hypnogram_5min'] = ['DLRA'[int(c)-1] for c in row['hypnogram_5min']]
        row['is_longest'] = bool(row['is_longest'])
        row['bedtime_start'] = dateutil.parser.parse(row['bedtime_start'])
        row['bedtime_end'] = dateutil.parser.parse(row['bedtime_end'])
        row['summary_date'] = dateutil.parser.parse(row['summary_date']).date()

    return data


def transform_activity_data(data):
    for row in data:
        row['class_5min'] = list(map(int, row['class_5min']))
        row['day_start'] = dateutil.parser.parse(row['day_start'])
        row['day_end'] = dateutil.parser.parse(row['day_end'])
        row['summary_date'] = dateutil.parser.parse(row['summary_date']).date()

    return data


def transform_readiness_data(data):
    return data
"""
main.py

Loads yesterday's personal Oura Ring data, and loads it into a data warehouse.
"""

import os

import psycopg2

from extract import load_daily_data
from transform import transform_sleep_data
from transform import transform_activity_data
from transform import transform_readiness_data
from load import upload_row


def main():
    """Perform ETL on Oura Ring data."""
    data = load_daily_data()

    sleep_data = transform_sleep_data(data['sleep'])
    activity_data = transform_activity_data(data['activity'])
    readiness_data = transform_readiness_data(data['readiness'])

    connection = psycopg2.connect(
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        host=os.environ.get('DB_HOST'),
        port=os.environ.get('DB_PORT'),
        database=os.environ.get('DB_DATABASE'))

    for row in sleep_data:
        upload_row('oura_sleep', row, connection)
    for row in activity_data:
        upload_row('oura_activity', row, connection)
    for row in readiness_data:
        upload_row('oura_readiness', row, connection)

    connection.commit()

    
if __name__ == "__main__":
    main()
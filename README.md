# Oura Ring API ETL

The [Oura Ring](https://ouraring.com/) is a powerful sleep and activity tracker. This project uses the [Oura Ring API](https://cloud.ouraring.com/) to load all of the previous day's sleep, readiness, and activity data, and stores it in a custom data warehouse.

## Installation

Note that this project requires Python 3.

### Installing prerequisites

```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

### Set up the data warehouse

The included file `setup_tables.sql` contains SQL commands for creating database tables that can store Oura data. Note that it uses some features specific to PostgreSQL.

### Create a launch script

Fill in the information in `run_etl.sh`, which involves your Oura and database credentials.

## Usage

```
./run_etl.sh
```
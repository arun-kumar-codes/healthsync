import psycopg2
from psycopg2 import sql
import requests
import json
from fastapi import HTTPException

class DataAggregator:
    def __init__(self, db_config):
        self.connection = self.create_connection(db_config)

    def create_connection(self, db_config):
        try:
            conn = psycopg2.connect(
                dbname=db_config['dbname'],
                user=db_config['user'],
                password=db_config['password'],
                host=db_config['host'],
                port=db_config['port']
            )
            return conn
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")

    def fetch_health_data(self, source_url):
        try:
            response = requests.get(source_url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error fetching data from {source_url}: {str(e)}")

    def aggregate_data(self, sources):
        aggregated_data = []
        for source in sources:
            data = self.fetch_health_data(source)
            aggregated_data.extend(data)
        return aggregated_data

    def save_to_database(self, data):
        try:
            with self.connection.cursor() as cursor:
                insert_query = sql.SQL("INSERT INTO health_data (source, data) VALUES (%s, %s)")
                for entry in data:
                    cursor.execute(insert_query, (entry['source'], json.dumps(entry['data'])))
                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise HTTPException(status_code=500, detail=f"Error saving data to database: {str(e)}")

    def run_aggregation(self, sources):
        aggregated_data = self.aggregate_data(sources)
        self.save_to_database(aggregated_data)

    def close_connection(self):
        if self.connection:
            self.connection.close()
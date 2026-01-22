import psycopg2
from psycopg2 import sql
import requests
import json
from fastapi import HTTPException

class DataAggregator:
    def __init__(self, db_config):
        self.connection = psycopg2.connect(**db_config)

    def fetch_health_data(self, source_url):
        try:
            response = requests.get(source_url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error fetching data from {source_url}: {str(e)}")

    def aggregate_data(self, sources):
        aggregated_data = []
        for source in sources:
            data = self.fetch_health_data(source)
            aggregated_data.extend(data.get('results', []))
        return aggregated_data

    def save_to_database(self, data):
        with self.connection.cursor() as cursor:
            for entry in data:
                try:
                    cursor.execute(
                        sql.SQL("INSERT INTO health_data (patient_id, health_metric, value) VALUES (%s, %s, %s) ON CONFLICT (patient_id) DO UPDATE SET health_metric = EXCLUDED.health_metric, value = EXCLUDED.value"),
                        (entry['patient_id'], entry['health_metric'], entry['value'])
                    )
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Error saving data to database: {str(e)}")
            self.connection.commit()

    def aggregate_and_store(self, sources):
        try:
            aggregated_data = self.aggregate_data(sources)
            self.save_to_database(aggregated_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error during data aggregation: {str(e)}")
        finally:
            self.connection.close()
import pandas as pd

from database_connection.db import Connection

class Scatter:
    def __init__(self, db_connect=Connection()):
        self.db_connect = db_connect

    def access_db(self):
        postgres_data = self.db_connect.connection()

        cur = postgres_data.cursor()
        cur.execute(
            '''select
            "latitude",
            "longitude",
            "geoapi_id"
            from "Response"
            limit 5000
            ''', postgres_data)

        data = cur.fetchall()

        return data

    @staticmethod
    def api_service_per_state():
        data = Scatter().access_db()

        api_service_per_state_df = pd.DataFrame(data, columns=['latitude', 'longitude', 'geoapi'])
        api_service_per_state_df['geoapi'] = api_service_per_state_df['geoapi'].apply(
            lambda x: x.astype(str).str.lower()
        )

        return api_service_per_state_df
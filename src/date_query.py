import pandas as pd

from db import Connection

class Date:
    def __init__(self, db_connect=Connection()):
        self.db_connect = db_connect

    def access_db(self):
        postgres_data = self.db_connect.connection()

        cur = postgres_data.cursor()

        cur.execute(
            '''select
            "date",
            "request_id",
            "geoapi_id"
            from "Search"
            limit(5000)''', postgres_data
        )

        data = cur.fetchall()

        return data

    @staticmethod
    def api_date():
        data = Date().access_db()

        convert_date = pd.DataFrame(data, columns=['date'])
        convert_date = pd.to_datetime(convert_date['date']).dt.date
        convert_date = pd.to_numeric(convert_date['date'])

        df = pd.DataFrame(data, columns=['request_id', 'geoapi_id'])
        df['date'] = convert_date['date']
        #df = pd.DataFrame(df, columns=['date', 'request_id', 'geoapi_id'])

        return df
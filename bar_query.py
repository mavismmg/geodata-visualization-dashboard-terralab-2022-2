import pandas as pd

from db import Connection

class Bar:
    def __init__(self, db_connect=Connection()):
        self.db_connect = db_connect

    def access_db(self):        
        postgres_data = self.db_connect.connection()

        cur = postgres_data.cursor()

        cur.execute(
            '''select
            "state",
            "geoapi_id",
            count(geolocation_id)
            from "Response"
            group by "state",
            "geoapi_id"''', postgres_data)

        data = cur.fetchall()

        return data


    @staticmethod
    def api_serviceCount_per_state():
        data = Bar().access_db()

        df = pd.DataFrame(data, columns=['state', 'geoapi_id', 'count'])

        df = df.apply(lambda x: x.astype(str).str.lower())

        # replace_dict = {
        #     'state of ': '',
        #     'federal district': 'distrito federal',
        #     'í': 'i',
        #     'á': 'a',
        #     'ã': 'a',
        #     'ô': 'o'
        # }

        # for state in df:
        #     df[state] = df[state].str.replace(state, replace_dict)

        df['state'] = df['state'].str.replace('state of ', '')
        df['state'] = df['state'].str.replace('federal district', 'distrito federal')
        df['state'] = df['state'].str.replace('í', 'i')
        df['state'] = df['state'].str.replace('á', 'a')
        df['state'] = df['state'].str.replace('ã', 'a')
        df['state'] = df['state'].str.replace('ô', 'o')

        pd.set_option('display.max_rows', None)

        df = df.drop(labels=[8, 58, 98, 133, 134, 139])

        api_serviceCount_per_state_df = pd.DataFrame(df, columns=[
                                                         'state',
                                                         'geoapi_id',
                                                         'count'])

        return api_serviceCount_per_state_df
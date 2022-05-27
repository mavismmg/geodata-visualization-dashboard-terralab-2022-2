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
            count(number)
            from "Request"
            group by "state"''', postgres_data)

        request_data = cur.fetchall()

        cur.execute(
            '''select
            "geoapi_id"
            from "Geoapi"
            '''
        )

        geoapi_data = cur.fetchall()

        return request_data, geoapi_data


    @staticmethod
    def api_serviceCount_per_state():
        request_data, geoapi_data = Bar().access_db()

        df = pd.DataFrame(request_data, columns=['state', 'count'])
        df = df.apply(lambda x: x.astype(str).str.lower())

        temp_df = pd.DataFrame(geoapi_data, columns=['geoapi_id'])

        df['geoapi_id'] = temp_df['geoapi_id']     

        df['state'] = df['state'].str.replace('state of ', '')
        df['state'] = df['state'].str.replace('federal district', 'distrito federal')
        df['state'] = df['state'].str.replace('í', 'i')
        df['state'] = df['state'].str.replace('á', 'a')
        df['state'] = df['state'].str.replace('ã', 'a')
        df['state'] = df['state'].str.replace('ô', 'o')

        state_initials_map = {
            'acre': 'ac',
            'alagoas': 'al',
            'amapa': 'ap',
            'amazonas': 'am',
            'amazonas': 'am',
            'bahia': 'ba',
            'ceara': 'ce',
            'distrito federal': 'df',
            'espirito santo': 'es',
            'goias': 'go',
            'maranhao': 'ma',
            'mato grosso': 'mt',
            'mato grosso do sul': 'ms',
            'minas gerais': 'mg',
            'para': 'pa',
            'paraiba': 'pb',
            'parana': 'pr',
            'pernambuco': 'pe',
            'piaui': 'pi',
            'rio de janeiro': 'rj',
            'rio grande do norte': 'rn',
            'rio grande do sul': 'rs',
            'rondonia': 'ro',
            'roraima': 'rr',
            'santa catarina': 'sc',
            'sao paulo': 'sp',
            'sergipe': 'se',
            'tocantins': 'to'
        }

        df = df.replace({'state': state_initials_map})

        pd.set_option('display.max_rows', None)

        df = df.drop(labels=[4])
        df['state'] = df['state'].apply(
            lambda x: x.upper()
        )

        api_serviceCount_per_state_df = pd.DataFrame(df, columns=[
                                                         'state',
                                                         'geoapi_id',
                                                         'count'])

        api_serviceCount_per_state_df.columns = ['Estado', 'Geoapi_id',
                                                 'Geocodificações concluídas']

        return api_serviceCount_per_state_df
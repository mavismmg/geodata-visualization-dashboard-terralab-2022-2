import pandas as pd

from db import Connection

class Chropleth:
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

        data = cur.fetchall()

        return data


    @staticmethod
    def geoapi():
        data = Chropleth().access_db()

        df = pd.DataFrame(data, columns=['state', 'count'])
        df = df.apply(lambda x: x.astype(str).str.lower()) 

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
        df['count'] = pd.to_numeric(df['count'])

        aggregation_map = {
            'state': 'first',
            'count': 'sum'
        }

        df = df.groupby('state', as_index=False).aggregate(aggregation_map)
        df = df.drop(labels=[0])
        df = df.apply(lambda x: x.astype(str).str.upper())
        
        geoapi_df = pd.DataFrame(df, columns=['state', 'count'])
        geoapi_df.columns = ['sigla', 'Buscas concluídas']

        # state_fullname_map = {
        #     'Acre',
        #     'Alagoas',
        #     'Amapa',
        #     'Amazonas',
        #     'Amazonas',
        #     'Bahia',
        #     'Aeara',
        #     'Distrito federal',
        #     'Espirito Santo',
        #     'Goias',
        #     'Maranhao', 
        #     'Mato Grosso',
        #     'Mato Grosso do Sul',
        #     'Minas Gerais',
        #     'Para',
        #     'Paraiba',
        #     'Parana',
        #     'Pernambuco',
        #     'Piaui',
        #     'Rio de Janeiro',
        #     'Rio Grande do Norte', 
        #     'Rio Grande do Sul', 
        #     'Rondonia',
        #     'Roraima',
        #     'Santa Catarina',
        #     'Sao Paulo',
        #     'Sergipe',
        #     'Tocantins',
        # }

        #state_name_df = pd.DataFrame.from_dict(state_fullname_map, columns=['Estado'])
        #geoapi_df['Estado'] = state_name_df['Estado']

        return geoapi_df
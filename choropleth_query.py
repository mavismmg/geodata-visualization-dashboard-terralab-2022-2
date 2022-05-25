import pandas as pd

from db import Connection

db_connect = Connection()

conn = db_connect.connection()

cur = conn.cursor()

cur.execute(
    '''select
    "state",
    count(geolocation_id)
    from "Response"
    group by "state"
    ''', conn)

test = cur.fetchall()

df = pd.DataFrame(test, columns=['state', 'count'])

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

new_df = df.groupby('state', as_index=False).aggregate(aggregation_map)
new_df = new_df.drop(labels=[3, 12, 15, 24, 30])

new_df = new_df.apply(lambda x: x.astype(str).str.upper())

geoapi_df = pd.DataFrame(new_df, columns=['state', 'count'])
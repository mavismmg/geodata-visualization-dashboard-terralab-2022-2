import pandas as pd

from db import Connection

db_connect = Connection()

conn = db_connect.connection()

cur = conn.cursor()

cur.execute(
    '''select
    "state",
    "geoapi_id",
    count(geolocation_id)
    from "Response"
    group by "state",
    "geoapi_id"
    ''', conn)

data = cur.fetchall()

temp_df = pd.DataFrame(data, columns=['state', 'geoapi_id', 'count'])

temp_df = temp_df.apply(lambda x: x.astype(str).str.lower())

temp_df['state'] = temp_df['state'].str.replace('state of ', '')
temp_df['state'] = temp_df['state'].str.replace('federal district', 'distrito federal')
temp_df['state'] = temp_df['state'].str.replace('í', 'i')
temp_df['state'] = temp_df['state'].str.replace('á', 'a')
temp_df['state'] = temp_df['state'].str.replace('ã', 'a')
temp_df['state'] = temp_df['state'].str.replace('ô', 'o')

pd.set_option('display.max_rows', None)

temp_df = temp_df.drop(labels=[8, 58, 98, 133, 134, 139])

api_serviceCount_per_state_df = pd.DataFrame(temp_df, columns=['state', 'geoapi_id', 'count'])
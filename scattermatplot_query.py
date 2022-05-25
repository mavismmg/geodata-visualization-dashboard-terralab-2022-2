import pandas as pd

from db import Connection

db_connect = Connection()

conn = db_connect.connection()

cur = conn.cursor()

cur.execute(
    '''select
    "latitude",
    "longitude",
    "geoapi_id"
    from "Response"
    limit 5000
    ''')

data = cur.fetchall()

api_service_per_state_df = pd.DataFrame(data, columns=['latitude', 'longitude', 'geoapi'])

# api_service_per_state_df = api_service_per_state_df.apply(
#     lambda x: x.astype(str).str.lower())
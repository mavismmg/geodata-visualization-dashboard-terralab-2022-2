from dash import Dash, dcc, html, Input, Output

import plotly.graph_objects as go
import pandas as pd
import psycopg2
import numpy as np
import plotly.express as px
import json

from urllib.request import urlopen
from choropleth_query import geoapi_df
from scattermatplot_query import api_service_per_state_df
from bar_query import api_serviceCount_per_state_df

app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='chropleth_plot'),
    dcc.Graph(id='scatter_plot'),
    dcc.Graph(id='bar_plot')
])

@app.callback(
    Output('graph', 'figure'),
    Output('graph2', 'figure'),
    Input('slider', 'value'))
def load_map():
    with urlopen('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson') as response:
        geo_map = json.load(response)

    # state_id_map = {}

    # for feature in brazil['features']:
    #     feature['id'] = feature['properties']['name']
    #     state_id_map[feature['properties']['sigla']] = feature['id']

    return geo_map


def chropleth_plot():
    geo_map = load_map()

    fig = px.choropleth_mapbox(
        geoapi_df, geojson=geo_map, locations='state',
        mapbox_style="carto-darkmatter", color='count',
        center={"lat": -14.6633, "lon": -53.54627}, zoom=3)

    #fig.update_geos(fitbounds="locations", visible=False)
    #fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig


def scatter_plot():
    fig = px.scatter_mapbox(
            api_service_per_state_df, lat=api_service_per_state_df['latitude'], lon=api_service_per_state_df['longitude'],
            color=api_service_per_state_df['geoapi'], mapbox_style="carto-darkmatter"
        )

    return fig


def bar_plot():
    fig = px.bar(api_serviceCount_per_state_df, x='state', y='count', color='geoapi_id')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
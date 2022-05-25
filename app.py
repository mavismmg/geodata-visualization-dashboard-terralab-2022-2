from datetime import date
from dash import Dash, dcc, html, Input, Output

import plotly.graph_objects as go
import pandas as pd
import psycopg2
import numpy as np
import plotly.express as px
import json

from urllib.request import urlopen
from choropleth_query import Chropleth
from scattermatplot_query import Scatter
from bar_query import Bar
from date_query import Date

app = Dash(__name__)

date = Date().api_date()

app.layout = html.Div([
    dcc.Graph(id='chropleth_plot'),
    dcc.Graph(id='scatter_plot'),
    dcc.Graph(id='bar_plot'),
    dcc.Graph(id='test_plot'),
    dcc.Slider(
        date['date'].min(),
        date['date'].max(),
        step=None,
        value=date['date'].min(),
        marks={str(date): str(date) for date in date['date'].unique()},
        id='date-slider'
    )
])

@app.callback(
    Output('chropleth_plot', 'figure'),
    Output('scatter_plot', 'figure'),
    Output('bar_plot', 'figure'),
    Output('test_plot', 'figure'),
    Input('date-slider', 'value'))
# def update_figure(selected_date):
#     geo_map = load_map()

#     ch_df = Chropleth().geoapi()

#     fig = px.choropleth_mapbox(
#         ch_df, geojson=geo_map, locations='state',
#         mapbox_style="carto-darkmatter", color='count',
#         center={"lat": -14.6633, "lon": -53.54627}, zoom=3)

#     filtered_df = date[date.date == selected_date]
    
#     filtered_scatter = px.scatter(filtered_df, x='geoapi_id', y='request_id',
#                                   color='date')

#     filtered_scatter.update_layout(transition_duration=500)

#     sc = Scatter().api_service_per_state()

#     scatter = px.scatter_mapbox(
#             sc, lat=sc['latitude'], lon=sc['longitude'],
#             color=sc['geoapi'], mapbox_style="carto-darkmatter"
#         )

#     ba = Bar().api_serviceCount_per_state()
#     bar = px.bar(ba, x='state', y='count', color='geoapi_id')

#     return fig, filtered_scatter, scatter, bar


def load_map():
    with urlopen('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson') as response:
        geo_map = json.load(response)

    # state_id_map = {}

    # for feature in brazil['features']:
    #     feature['id'] = feature['properties']['name']
    #     state_id_map[feature['properties']['sigla']] = feature['id']

    return geo_map


def test_plot(selected_date):
    filtered_df = date[date.date == selected_date]

    fig = px.scatter(filtered_df, x='geoapi_id', y='request_id',
                     color='date')

    fig.update_layout(transition_duration=500)

    return fig


def chropleth_plot():
    df = Chropleth().geoapi()
    geo_map = load_map()

    fig = px.choropleth_mapbox(
        df, geojson=geo_map, locations='state',
        mapbox_style="carto-darkmatter", color='count',
        center={"lat": -14.6633, "lon": -53.54627}, zoom=3)

    return fig


def scatter_plot():
    df = Scatter().api_service_per_state()
    fig = px.scatter_mapbox(
            df, lat=df['latitude'], lon=df['longitude'],
            color=df['geoapi'], mapbox_style="carto-darkmatter"
        )

    return fig


def bar_plot():
    df = Bar().api_serviceCount_per_state()
    fig = px.bar(df, x='state', y='count', color='geoapi_id')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
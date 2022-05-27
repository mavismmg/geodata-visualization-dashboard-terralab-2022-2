from email.mime import application
from tracemalloc import start
from dash import Dash, dcc, html, Input, Output, callback_context
from urllib.request import urlopen
from datetime import date

import plotly.graph_objects as go
import plotly.express as px
import json

from choropleth_query import Chropleth
from scattermatplot_query import Scatter
from bar_query import Bar

class ApplicationDashboard:
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = Dash(__name__, external_stylesheets=external_stylesheets)

    def __init__(self, chropleth_df=Chropleth().geoapi(), scatter_df=Scatter().api_service_per_state(), bar_df=Bar().api_serviceCount_per_state()):
        self.chropleth_df = chropleth_df
        self.scatter_df = scatter_df
        self.bar_df = bar_df

        self.app.layout = html.Div(
            [
                dcc.DatePickerRange(
                    id='display-data-by-date',
                    min_date_allowed=('2022, 2, 9'),
                    max_date_allowed=('2022, 4, 25'),
                    initial_visible_month=('2022, 2, 9'),
                    end_date=date(2022, 2, 9),
                    display_format='MMM Do, YY',
                    month_format='MMMM, YYYY',
                    number_of_months_shown=1,
                    updatemode='singledate'
                ),
                html.Div(id='output-container-display-data-by-date'),
                dcc.Graph(id='chropleth_plot'),
                dcc.Graph(id='scatter_plot'),
                dcc.Graph(id='bar_plot'),
            ]
        )

        if self.app is not None and hasattr(self, "callbacks"):
            self.callbacks(self.app)
    
    def callbacks(self, app):
        @app.callback(
            Output('chropleth_plot', 'figure'),
            Output('scatter_plot', 'figure'),
            Output('bar_plot', 'figure'),
            Input('display-data-by-date', 'start_date'),
            Input('display-data-by-date', 'end_date'))
        def update_output(start_date, end_date):
            geo_map = ApplicationDashboard().load_map()

            self.update(start_date, end_date)

            map_fig = px.choropleth_mapbox(
                self.chropleth_df, geojson=geo_map, locations="sigla",
                mapbox_style="carto-positron", color="Buscas concluídas",
                center={"lat": -14.6633, "lon": -53.54627}, zoom=3, featureidkey="properties.sigla",
                hover_name="sigla")

            scatter_fig = px.scatter_mapbox(
                    self.scatter_df, lat=self.scatter_df["latitude"],
                    lon=self.scatter_df["longitude"], color=self.scatter_df["geoapi"], 
                    mapbox_style="carto-positron", hover_name="geoapi"
                )

            bar_fig = px.bar(self.bar_df, x="Estado", y="Geocodificações concluídas", color='Geoapi_id',
                            text="Geocodificações concluídas", hover_name="Geoapi_id")

            return map_fig, scatter_fig, bar_fig

    def update(self, start_date, end_date):
        self.chropleth_df = self.chropleth_df.loc[start_date:end_date]
        self.scatter_df = self.scatter_df.loc[start_date:end_date]
        self.bar_df = self.bar_df.loc[start_date:end_date]

    @staticmethod
    def load_map():
        with urlopen('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson') as response:
            geo_map = json.load(response)

        state_id_map = {}

        for feature in geo_map['features']:
            feature['id'] = feature['properties']['name']
            state_id_map[feature['properties']['sigla']] = feature['id']

        return geo_map

    def start(self):
        self.app.run_server(debug=True)
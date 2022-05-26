from dash import Dash, dcc, html, Input, Output

import plotly.graph_objects as go
import plotly.express as px
import json

from urllib.request import urlopen
from choropleth_query import Chropleth
from scattermatplot_query import Scatter
from bar_query import Bar
#from date_query import Date

app = Dash(__name__)

class Geo:
    def __init__(self,
        chropleth_df=Chropleth().geoapi(),
        scatter_df=Scatter().api_service_per_state(),
        bar_df=Bar().api_serviceCount_per_state()):

        self.chropleth_df = chropleth_df
        self.scatter_df = scatter_df
        self.bar_df = bar_df

    
    @staticmethod
    def load_map():
        with urlopen('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson') as response:
            geo_map = json.load(response)

        state_id_map = {}

        for feature in geo_map['features']:
            feature['id'] = feature['properties']['name']
            state_id_map[feature['properties']['sigla']] = feature['id']

        return geo_map

    
    def update_figure(self):
        geo_map = Geo().load_map()

        map_fig = px.choropleth_mapbox(
            self.chropleth_df, geojson=geo_map, locations='Estado',
            mapbox_style="carto-positron", color='Buscas concluídas',
            center={"lat": -14.6633, "lon": -53.54627}, zoom=3)

        scatter_fig = px.scatter_mapbox(
                self.scatter_df, lat=self.scatter_df['latitude'],
                lon=self.scatter_df['longitude'], color=self.scatter_df['geoapi'], 
                mapbox_style="carto-positron", size="geoapi", hover_name="geoapi"
            )

        bar_fig = px.bar(self.bar_df, x='Estado', y='Geocodificações concluídas', color='Geoapi_id',
                         text='Geocodificações concluídas')

        return map_fig, scatter_fig, bar_fig


map_fig, scatter_fig, bar_fig = Geo().update_figure()

app.layout = html.Div([
    dcc.Graph(id='chropleth_plot', figure=map_fig),
    dcc.Graph(id='scatter_plot', figure=scatter_fig),
    dcc.Graph(id='bar_plot', figure=bar_fig),
    #dcc.Graph(id='test_plot'),
])

if __name__ == '__main__':
    app.run_server(debug=True)
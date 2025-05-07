# callbacks.py
from dash.dependencies import Input, Output

import components.ch_map as map
import components.municipality_map as m_map

import components.fuel as fl
import plotly.express as px

def register_callbacks(app):
    '''
    Register all callbacks within this function
    :param app: Dash app instance
    :return: None
    '''

    @app.callback(
        Output('choropleth-map', 'figure'),
        Input('year-slider', 'value')
    )
    def update_map(selected_year):
        '''
        Callback to draw the ch map with data points of the selected year
        :param selected_year yyyy
        :returns a figure object
        '''
        fig = map.generate_ch_map(year=selected_year)
        return fig

    '''
    callback for choropleth map municipality
    '''
    @app.callback(
        Output('choropleth-map-municipality', 'figure'),
        [Input('year-slider', 'value'),
         Input('choropleth-map', 'clickData')]
    )
    def update_map(selected_year, clickData):
        '''
        Callback to draw the ch  municipality with data points of the selected year and clicked canton
        :param selected_year
        :param clickData clicked data on the ch map
        :returns a figure object
        '''

        # if nothing was clicked return an empty map
        if not clickData:
            return px.scatter_mapbox()

        # get canton based on clicked position on the CH map
        canton = clickData["points"][0]["location"]

        fig = m_map.generate_map_municipality(year=selected_year, canton=canton)
        return fig

    '''
    callback for stackedbar fuel (ivs: Inverkehrsetzungen)
    '''
    @app.callback(
        Output('stackedbar-fuel-ivs', 'figure'),
        Input('year-slider', 'value')
    )
    def update_charts_fuel_ivs(selected_year):
        '''
        Callback to draw the stackedbar fuel with data points of the selected year
        :param selected_year:
        :return: figure object
        '''
        stackedbar = fl.generate_stacked_bar_fuel_ivs(fl.df_fuel, selected_year)
        return stackedbar

    @app.callback(
        Output('stackedbar-fuel-stock', 'figure'),
        Input('year-slider', 'value')
    )
    def update_charts_fuel_stock(selected_year):
        '''
        Callback to draw the stackedbar fuel with data points of the selected year
        :param selected_year:
        :return: figure object
        '''
        stackedbar = fl.generate_stacked_bar_fuel_stock(fl.df_fuel, selected_year)
        return stackedbar

    @app.callback(
        Output('multiline-total', 'figure'),
        Input('year-slider', 'value')
    )
    def update_charts_fuel_stock(selected_year):
        '''
        Callback to draw the multiline chart (ivs, stock)
        :param selected_year:
        :return:
        '''
        multiline = fl.generate_multiline_total(fl.df_fuel, selected_year)
        return multiline



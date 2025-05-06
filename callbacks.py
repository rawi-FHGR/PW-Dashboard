# callbacks.py
from dash.dependencies import Input, Output

import components.ch_map as map
import components.canton_map as c_map
import components.fuel as fl
import plotly.express as px

def register_callbacks(app):
    # Callback for updating the map

    '''
    callback for ch choropleth map
    :param app:
    :return:
    '''
    @app.callback(
        Output('choropleth-map', 'figure'),
        Input('year-slider', 'value')
    )
    def update_map(selected_year):
        '''
        Draws the ch map with data points of the selected year
        :param selected_year yyyy
        :returns a figure object
        '''
        fig = map.generate_ch_map(year=selected_year)
        return fig

    '''
    callback for choropleth map canton
    '''
    @app.callback(
        Output('choropleth-map-canton', 'figure'),
        [Input('year-slider', 'value'),
         Input('selected-canton-output', 'children')]
    )
    def update_map(selected_year, canton_text):

        # Kantonskürzel aus dem Text extrahieren
        if not canton_text.startswith('Ausgewählter Kanton:'):
            return px.scatter_mapbox()  # leer

        canton = canton_text.replace('Ausgewählter Kanton:', '').strip()

        fig = c_map.generate_map_canton(year=selected_year, canton=canton)
        return fig

    # Callback mit zwei Outputs
    @app.callback(
        Output('stackedbar-fuel-ivs', 'figure'),
        Input('year-slider', 'value')
    )
    def update_charts_fuel_ivs(selected_year):
        stackedbar = fl.generate_stacked_bar_fuel_ivs(fl.df_fuel, selected_year)
        return stackedbar

    @app.callback(
        Output('stackedbar-fuel-stock', 'figure'),
        Input('year-slider', 'value')
    )
    def update_charts_fuel_stock(selected_year):
        stackedbar = fl.generate_stacked_bar_fuel_stock(fl.df_fuel, selected_year)
        return stackedbar

    @app.callback(
        Output('multiline-total', 'figure'),
        Input('year-slider', 'value')
    )
    def update_charts_fuel_stock(selected_year):
        stackedbar = fl.generate_multiline_total(fl.df_fuel, selected_year)
        return stackedbar


    '''
    callback: output selected canton in text form
    '''
    @app.callback(
        Output('selected-canton-output', 'children'),
        Input('choropleth-map', 'clickData')
    )
    def display_selected_canton(clickData):
        if clickData and 'points' in clickData:
            canton = clickData['points'][0]['location']
            return f'Ausgewählter Kanton: {canton}'
        return 'Kein Kanton gewählt.'

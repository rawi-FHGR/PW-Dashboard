# callbacks.py
from dash.dependencies import Input, Output
import plotly.express as px
import inspect
import dash.html as html
import dash.dcc as dcc

import logging

# import components
import components.ch_map as map
import components.municipality_map as m_map
import components.fuel as fl
import components.infobox as info

# initialize logger
logger = logging.getLogger(__name__)

def register_callbacks(app):
    '''
    Register all callbacks within this function
    :param app: Dash app instance
    :return: None
    '''

    @app.callback(
        Output('choropleth-map', 'figure'),
        [Input('year-slider', 'value'),
         Input('value-mode-toggle', 'value')]
    )
    def update_map(selected_year, is_relative):
        '''
        Callback to draw the ch map with data points of the selected year
        :param selected_year yyyy
        :returns a figure object
        '''
        fig = map.generate_ch_map(year=selected_year, is_relative=is_relative)
        return fig

    @app.callback(
        Output('choropleth-map-municipality', 'figure'),
        [Input('year-slider', 'value'),
         Input('selected-canton', 'data'),
         Input('value-mode-toggle', 'value')]
    )
    def update_map(selected_year, canton, is_relative):
        '''
        Callback to draw the ch municipality with data points of the selected year and clicked canton
        :param selected_year
        :param clickData clicked data on the ch map
        :returns a figure object
        '''

        # if nothing was clicked (canton=CH) return an empty map
        if canton == 'CH':
            return px.scatter_mapbox()

        # generate map of the selected canton
        return m_map.generate_map_municipality(year=selected_year, canton=canton, is_relative=is_relative)

    @app.callback(
        Output('stackedbar-fuel-stock-canton', 'figure'),
        [Input('year-slider', 'value'),
         Input('selected-canton', 'data'),
         Input('value-mode-toggle', 'value')]
    )
    def update_charts_fuel_stock_canton(selected_year, canton, is_relative):
        '''
        Callback to draw the stackedbar fuel with data points of the selected year
        :param selected_year:
        :return: figure object
        '''

        # if nothing was clicked (canton=CH) return an empty map
        if canton == 'CH':
            return fl.generate_stacked_bar_fuel_stock(fl.df_fuel, selected_year, is_relative)

        # generate and return stacked bar chart for the selected canton
        return fl.generate_stacked_bar_fuel_stock_canton(fl.df_fuel, selected_year, canton, is_relative)

    @app.callback(
        Output('pie-fuel-stock', 'figure'),
        [Input('year-slider', 'value'),
         Input('selected-canton', 'data'),
         Input('value-mode-toggle', 'value')]
    )
    def update_pie_fuel(selected_year, canton, is_relative):
        df_jahr = fl.df_fuel[fl.df_fuel["Jahr"] == selected_year]

        # if nothing was clicked (canton=CH) return an empty map
        if canton == 'CH':
            return fl.generate_pie_fuel_stock(df_jahr, selected_year, is_relative)

        # generate and return pie chart for the selected canton
        return fl.generate_pie_fuel_stock_canton(df_jahr, selected_year, canton, is_relative)

    @app.callback(
        Output('summary-container', 'children'),
        [Input('year-slider', 'value'),
         Input('selected-canton', 'data'),
         Input('value-mode-toggle', 'value')]
    )
    def update_summary(selected_year, canton, is_relative):
        '''
        Callback to display the data summary of the selected year and canton
        :param year: selected year
        :param canton: selected canton
        :param is_relative: state of the toggle switch (to change the data mode absolute and relative)
        :return:
        '''
        df_year = fl.df_fuel[fl.df_fuel["Jahr"] == selected_year]

        if canton == 'CH':
            return fl.generate_fuel_summary_text_CH(df_year, selected_year, is_relative)

        return fl.generate_fuel_summary_text_canton(df_year, selected_year, canton, is_relative)


    # callback for handling the upper right field which changes the display type at runtime
    @app.callback(
        Output('right-panel', 'children'),
        [Input('selected-canton', 'data'),
         Input('year-slider', 'value'),
         Input('value-mode-toggle', 'value')]
    )
    def update_right_panel(canton, selected_year, is_relative):
        logger.debug(f'right panel update: {canton}, {selected_year}, {is_relative}')

        # no canton seleceted -> show info text
        if canton == 'CH' or canton is None:
            return info.display_info_text()

        # display the map if a canton was selected
        fig = m_map.generate_map_municipality(year=selected_year, canton=canton, is_relative=is_relative)
        return dcc.Graph(figure=fig, style={'height': '100%'})


    # hidden callbacks
    # Callback 1: clickData → Store
    @app.callback(
        Output("selected-canton", "data"),
        Input("choropleth-map", "clickData")
    )
    def extract_kanton(clickData):
        # if nothing was clicked return CH for different handling
        if clickData is None:
            return "CH"
        # get canton based on clicked position on the CH map and return it
        return clickData['points'][0]['location']





    # @app.callback(
    #     Output('stackedbar-fuel-ivs', 'figure'),
    #     Input('year-slider', 'value')
    # )
    # def update_charts_fuel_ivs(selected_year):
    #     '''
    #     Callback to draw the stackedbar fuel with data points of the selected year
    #     :param selected_year:
    #     :return: figure object
    #     '''
    #     stackedbar = fl.generate_stacked_bar_fuel_ivs(fl.df_fuel, selected_year)
    #     return stackedbar

    # @app.callback(
    #     Output('stackedbar-fuel-stock', 'figure'),
    #     Input('year-slider', 'value')
    # )
    # def update_charts_fuel_stock(selected_year):
    #     '''
    #     Callback to draw the stackedbar fuel with data points of the selected year
    #     :param selected_year:
    #     :return: figure object
    #     '''
    #     stackedbar = fl.generate_stacked_bar_fuel_stock(fl.df_fuel, selected_year)
    #     return stackedbar
    #
    # @app.callback(
    #     Output('multiline-total', 'figure'),
    #     Input('year-slider', 'value')
    # )
    # def update_charts_fuel_stock(selected_year):
    #     '''
    #     Callback to draw the multiline chart (ivs, stock)
    #     :param selected_year:
    #     :return:
    #     '''
    #     multiline = fl.generate_multiline_total(fl.df_fuel, selected_year)
    #     return multiline

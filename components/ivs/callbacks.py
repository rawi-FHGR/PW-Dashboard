# callbacks.py
from helper.general import default_year
from dash.dependencies import Input, Output
import plotly.express as px
import dash.dcc as dcc
from dash import callback_context
import dash

import logging

# import components
import components.ivs.ch_map as map
import components.ivs.canton_map as m_map
import components.ivs.fuel as fl
import components.infobox as info

# initialize logger
from helper.misc import log_current_function
logger = logging.getLogger(__name__)

def register_callbacks(app):
    '''
    Register all callbacks within this function
    :param app: Dash app instance
    :return: None
    '''
    log_current_function(level=logging.INFO, msg=f"{__name__}")


    @app.callback(
        Output('choropleth-map-ivs', 'figure'),
        [Input('year-slider-ivs', 'value'),
         Input('value-mode-toggle-ivs', 'value')]
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
        Output('choropleth-map-municipality-ivs', 'figure'),
        [Input('year-slider-ivs', 'value'),
         Input('selected-canton-ivs', 'data'),
         Input('value-mode-toggle-ivs', 'value')]
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
        return m_map.generate_map_canton(year=selected_year, canton=canton, is_relative=is_relative)

    @app.callback(
        Output('stackedbar-fuel-stock-canton-ivs', 'figure'),
        [Input('year-slider-ivs', 'value'),
         Input('selected-canton-ivs', 'data'),
         Input('value-mode-toggle-ivs', 'value')]
    )
    def update_stackedbar_fuel(selected_year, canton, is_relative):
        '''
        Callback to draw the stackedbar fuel with data points of the selected year
        :param selected_year:
        :return: figure object
        '''

        # generate and return stacked bar chart for the selected canton (CH if no canton was selected)
        return fl.generate_stacked_bar_fuel(fl.df_fuel, selected_year, canton, is_relative)

    @app.callback(
        Output('pie-fuel-stock-ivs', 'figure'),
        [Input('year-slider-ivs', 'value'),
         Input('selected-canton-ivs', 'data'),
         Input('value-mode-toggle-ivs', 'value')]
    )
    def update_pie_fuel(selected_year, canton, is_relative):
        df_jahr = fl.df_fuel

        # generate and return pie chart for the selected canton
        return fl.generate_pie_fuel(df_jahr, selected_year, canton, is_relative)

    @app.callback(
        Output('summary-container-ivs', 'children'),
        [Input('year-slider-ivs', 'value'),
         Input('selected-canton-ivs', 'data'),
         Input('value-mode-toggle-ivs', 'value')]
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

        return fl.generate_fuel_summary(df_year, selected_year, canton, is_relative)

    # callback for handling the upper right field which changes the display type at runtime
    @app.callback(
        Output('right-panel-ivs', 'children'),
        [Input('selected-canton-ivs', 'data'),
         Input('year-slider-ivs', 'value'),
         Input('value-mode-toggle-ivs', 'value')]
    )
    def update_right_panel(canton, selected_year, is_relative):
        logger.debug(f'right panel update: {canton}, {selected_year}, {is_relative}')

        # no canton selected -> show info text
        if canton == 'CH' or canton is None:
            return info.display_info_text()

        # display the map if a canton was selected
        fig = m_map.generate_map_canton(year=selected_year, canton=canton, is_relative=is_relative)
        return dcc.Graph(figure=fig, config={"scrollZoom": True}, style={'height': '100%'})

    @app.callback(
        Output("selected-canton-ivs", "data"),
        Output("year-slider-ivs", "value"),
        Output("value-mode-toggle-ivs", "value"),
        [Input("choropleth-map-ivs", "clickData"),
         Input("home-button-ivs", "n_clicks")],
        prevent_initial_call=True
    )
    def update_canton(clickData, home_clicks):
        ctx = callback_context

        if not ctx.triggered:
            raise dash.exceptions.PreventUpdate

        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if trigger_id == "choropleth-map-ivs":
            if clickData is None:
                return "CH", dash.no_update, dash.no_update
            return clickData['points'][0]['location'], dash.no_update, dash.no_update

        elif trigger_id == "home-button-ivs":
            return "CH", default_year, True


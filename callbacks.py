# callbacks.py
from dash.dependencies import Input, Output

import components.ch_map as map

def register_callbacks(app):
    # Callback for updating the map
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

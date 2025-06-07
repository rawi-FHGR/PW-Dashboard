# common definitions and functions for the components

# imports
import plotly.graph_objects as go

import logging
from helper.misc import log_current_function

import helper.general as gen

##################################
### variables / constants
##################################

logger = logging.getLogger(__name__)

color_fuel= {
    "Benzin": gen.colors['lightgrey'],
    "Diesel": gen.colors['brown'],
    "Hybrid": gen.colors['yellow'],
    "Elektrisch": gen.colors['teal'],
    "Andere": gen.colors['blue'],
    "Gas": gen.colors['brown'],
    "Wasserstoff": gen.colors['blue']
}

text_style = {
        'fontFamily': 'Arial, sans-serif',
        'fontSize': '0.9vw',
        'color': '#333333'
}

##################################
### functions
##################################

def add_year_marker(figure, year, y_max, color='red', annotation: str=''):
    """
    Adds a vertical marker (line and point) to a chart (given as figure object).
    Works also with categorical x-axis (strings).

    :param figure: Plotly figure object (e.g. px.bar)
    :param year: year, which will be marked (int or str)
    :param y_max: max y-size (for the vertical line)
    :param color: color of the marker
    :param annotation: annotation of the marker
    """
    log_current_function(level=logging.DEBUG, msg=f"{year}")

    # handle year as string
    year_str = str(year)

    # add marker circle
    figure.add_trace(go.Scatter(
        x=[year_str], y=[0],
        mode='markers',
        marker=dict(color=color, size=10, symbol='circle'),
        showlegend=False
    ))

    # add vertical marker line
    figure.add_trace(go.Scatter(
        x=[year_str, year_str],
        y=[0, y_max],
        mode='lines',
        line=dict(color=color, width=3),
        showlegend=False,
        hoverinfo='skip'
    ))

    # add optional annotation at top of marker line
    if annotation:
        figure.add_annotation(
            x=[year_str],
            y=1.08,
            xref='x',
            yref='paper',
            text=annotation,
            showarrow=False,
            font=dict(size=13),
            bgcolor=gen.hex_to_rgba_value(color, 0.1),    # or: white
            bordercolor=color,
            borderwidth=1,
            align='center'
        )


def get_current_annotations(annotations, canton, year) -> str:
    annotation_texts = ''
    # collect all annotation for the current year and canton
    for annotation in annotations:
        if annotation['kanton'] == canton:
            if annotation['jahr_von'] <= year <= annotation['jahr_bis']:
                annotation_texts += annotation['text'] + '<br>'

    return annotation_texts

def calculate_zoom_factor(width:float) -> float:
    zoom_factor = 1.0
    if width < 0.2:
        zoom_factor = 10
    elif width < 0.37:
        zoom_factor = 9
    elif width < 0.75:
        zoom_factor = 7.9
    elif width < 1:
        zoom_factor = 7.5
    elif width < 1.5:
        zoom_factor = 7
    else:
        zoom_factor = 6.9

    return zoom_factor
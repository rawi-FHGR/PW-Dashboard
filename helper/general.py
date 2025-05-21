import pandas as pd
import plotly.graph_objects as go

import logging

# import project specific settings and functions
from helper.misc import log_current_function
logger = logging.getLogger(__name__)

# general settings and functions

# functions
def hex_to_rgba_value(hex_color, alpha=0.4):
    '''
    Converts a hex-coded color into a RGBA string with transparency.
    :param hex_color: The hex color to convert
    :return a RGBA string
    '''
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"

def normalize_fuel_categories(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate some fuel categories in the given dataframe.
     - sum up hybrid categories and provide these in the column 'Hybrid'
     - sum up Anderer, Gas, ohne Motor, Wasserstoff and provide these in the column 'Andere'

    :param df: original dataframe
    :return: df: aggregated dataframeKopie des DataFrames mit aggregierter Spalte 'Treibstoff_mod'
    """
    hybrid_categories = {
        "Benzin-elektrisch: Normal-Hybrid",
        "Benzin-elektrisch: Plug-in-Hybrid",
        "Diesel-elektrisch: Normal-Hybrid",
        "Diesel-elektrisch: Plug-in-Hybrid"
    }

    other_categories = {
        "Anderer",
        "Gas (mono- und bivalent)",
        "Ohne Motor",
        "Wasserstoff"
    }

    # prepare an aggregation map to sum up the values for each new category
    aggregation_map = {
        **{category: "Hybrid" for category in hybrid_categories},
        **{category: "Andere" for category in other_categories}
    }

    df = df.copy()
    # overwrite the original column 'Treibstoff'
    df['Treibstoff'] = df['Treibstoff'].replace(aggregation_map)

    return df

def format_number(value: int, use_separator: bool = True) -> str:
    '''
    Converts a number into an appropriate formatted number.
    :param value:
    :param use_separator:
    :return: reformatted number
    '''
    if use_separator:
        return f"{int(value):,}".replace(",", "'")  # CH format
    return str(int(value))

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
            y=1.05,
            xref='x',
            yref='paper',
            text=annotation,
            showarrow=False,
            font=dict(size=13),
            bgcolor=hex_to_rgba_value(color, 0.1),    # or: white
            bordercolor=color,
            borderwidth=1,
            align='center'
        )

# settings
available_years = list(range(2010,2025,1))
default_year = 2024

# colormap
# colors = {
#     "blue": "#1f77b4",
#     "orange": "#ff7f0e",
#     "green": "#2ca02c",
#     "red": "#d62728",
#     "purple": "#9467bd",
#     "brown": "#8c564b",
#     "pink": "#e377c2",
#     "grey": "#7f7f7f"
# }

colors = {
    "blue": "#1f77b4",
    "orange": "orange",
    "green": "#4acf70",
    "cyan":"#45ddff",
    "red": "#fa114f",
    "purple": "#9467bd",
    "brown": "#8c564b",
    "pink": "#e377c2",
    "grey": "#7f7f7f",
    "black": "black"
}



if __name__ == "__main__":
    print(colors)
import dash
import dash_bootstrap_components as dbc
import logging

import plotly.express as px
import pandas as pd
import json

import helper.general as gen

from helper.misc import log_current_function
logger = logging.getLogger(__name__)

# variables
texts = {
    'map.title':'Fahrzeugbestand CH',
    'relative':'pro 1000',
    'inhabitant':'Einwohner',
    'cars': 'Personenwagen',
    'no_data_available': 'Keine Daten für das ausgewählte Jahr verfügbar',
    'title_colorbar':'Bestand'
}

data_columns = ['Kanton', 'DATA_Bestand', 'DATA_Bestand pro 1000']

# functions
def generate_ch_map(year: int, is_relative: bool=False):
    '''
    Draws a choropleth map of Switzerland with canton-specific data
    :param year: selected year
    :return: Plotly figure object
    '''
    log_current_function(level=logging.DEBUG, msg=f"{year} {is_relative}")

    if is_relative:
        title = f'<b>{texts.get("map.title")} {texts.get("relative")} {texts.get("inhabitant")} ({year})</b>'
        data_column = data_columns[2]
        hover_text = f'{texts.get("cars")} {texts.get("relative")} {texts.get("inhabitant")}'
    else:
        title = f'<b>{texts.get("map.title")} ({year})</b>'
        data_column = data_columns[1]
        hover_text = f'{texts.get("cars")}'

    # get only data for the selected year
    df_filtered = df[df['Kanton'] != 'CH']
    df_year = df_filtered[df_filtered['Jahr'] == year]

    # Check for empty data
    if df_year.empty:
        fig = go.Figure()
        fig.update_layout(
            title=f"<b>{texts.get('no_data_available')} ({year})</b>",
            title_x=0.5,
            title_font_size=16,
            margin={"r": 0, "t": 30, "l": 0, "b": 0}
        )
        return fig

    # Daten aggregieren
    df_grouped = df_year.groupby(['Jahr', 'Kanton'])[data_column].sum().reset_index()

    # prepare map
    fig = px.choropleth(
        df_grouped,
        geojson=geojson_data,
        locations=data_columns[0],
        featureidkey="properties.Kanton",
        color=data_column,
        hover_data={data_column: ':.2f'},
        color_continuous_scale="Viridis",
    )

    fig.update_geos(
        projection_type="conic conformal",
        projection_scale=140,
        # center CH
        center={"lat": 46.8, "lon": 8.3},
        visible=False
    )

    fig.update_layout(
        title=title,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        coloraxis_colorbar={
            "title": texts.get('title_colorbar'),
            "len": 0.75,
            "x": 0.85,
            "ticks": "outside",
            "tickformat": "~s",
            "xpad": 0,
            "yanchor": "middle",
            "xanchor": "left"
        },
        title_x=0.5,
        title_y=0.97,
        uirevision="constant"
    )

    # draw colored outlines
    fig.update_traces(marker_line_color=gen.colors['lightgrey'], marker_line_width=0.5)

    # tooltip setzen
    hovertemplate = (
        "<b>%{location}</b><br>"
        "%{z:.0f} " + hover_text + "<br>"
        "<extra></extra>"
    )
    fig.update_traces(hovertemplate=hovertemplate)

    return fig

# setup data
# read simplified GeoJSON to work locally
with open("./data/Geodaten_Kantone.geojson", encoding="utf-8") as f:
    geojson_data = json.load(f)

# get statistical data from file or database
df_csv= pd.read_csv('data/Autodaten_Kantone.csv', delimiter=',')

# provide the data as pandas dataframe
df = df_csv.fillna(0)
import dash
import dash_bootstrap_components as dbc
import logging

import plotly.express as px
import pandas as pd
import json

import helper.general as gen
import components.common as common

from helper.misc import log_current_function
logger = logging.getLogger(__name__)

# variables
texts = {'title':'Inverkehrsetzungen pro Gemeinde',
         'title_colorbar':'Anzahl',
         'relativ':'pro 1000 Einwohner',
         'inhabitant':'Einwohner'}

data_columns = ['Gemeindename', 'DATA_Inverkehrsetzung', 'DATA_Inverkehrsetzung pro 1000']

annotations = [
    {'kanton': 'BE', 'jahr_von': '2018', 'jahr_bis': '2018', 'text': 'Gründung von Carvolution in Bannwil.'},
    {'kanton': 'BE', 'jahr_von': '2019', 'jahr_bis': '2024',
     'text': 'Carvolution: stetige Zunahme des <br>Fahrzeugbestands in Bannwil'},
    {'kanton': 'ZG', 'jahr_von': '2010', 'jahr_bis': '2019',
     'text': 'Stetiger Flottenausbau von Arval (Hauptsitz = Halteradresse)'},
    {'kanton': 'ZG', 'jahr_von': '2018', 'jahr_bis': '2018',
     'text': 'Mobility von Luzern nach Risch  (Hauptsitz = Halteradresse)'},
    {'kanton': 'ZG', 'jahr_von': '2019', 'jahr_bis': '2019',
     'text': 'Arval von Cham nach Risch (Hauptsitz = Halteradresse)'},
    {'kanton': 'ZG', 'jahr_von': '2020', 'jahr_bis': '2024',
     'text': 'Stetiger Flottenausbau von Mobility und Arval (Hauptsitz = Halteradresse)'}
]

# functions
def generate_map_canton(year: int, canton: str, is_relative: bool=False):
    '''
    Draws a canton outline with municipality data
    :param year:
    :param canton:
    :return: figure object
    '''
    log_current_function(level=logging.DEBUG, msg=f"{year} {canton} {is_relative}")

    # use the right data depending on the data mode
    if is_relative:
        title = f'<b>{canton}: {texts.get("title")} {texts.get("relativ")} ({year})</b>'
        data_column = data_columns[2]
    else:
        title = f'<b>{canton}: {texts.get("title")} ({year})</b>'
        data_column = data_columns[1]

    # aggregate municipality data for the given year and canton
    df_cant = (
        df[(df['Kanton'] == canton) & (df['Jahr'] == year)]
        .groupby(['ID_Gemeinde', 'Gemeindename'], as_index=False)
        .agg({data_column: 'sum'})
    )

    # prevent application crash due to missing data
    if df_cant.empty:
        logger.warning(f'Keine Daten für diesen Kanton und Jahr. {canton}, {year}, {is_relative}')
        return px.scatter_mapbox()

    # convert attribute to a string
    df_cant['ID_Gemeinde'] = df_cant['ID_Gemeinde'].astype(str)

    # use only canton relevant geojson data
    canton_features = [
        f for f in geojson_data["features"]
        if f["properties"]["Kanton"] == canton
    ]
    # get municipality data for the selected canton
    for f in canton_features:
        f["properties"]["ID_Gemeinde"] = str(f["properties"]["ID_Gemeinde"])

    canton_geojson = {
        "type": "FeatureCollection",
        "features": canton_features
    }

    # "calculate" center and zoom for the canton illustration
    from shapely.geometry import shape
    from shapely.ops import unary_union

    geometries = [shape(f["geometry"]) for f in canton_features]
    union_geom = unary_union(geometries)
    minx, miny, maxx, maxy = union_geom.bounds
    center_coords = {"lat": (miny + maxy) / 2, "lon": (minx + maxx) / 2}
    bbox_width = maxx - minx
    zoom = 9 if bbox_width < 0.5 else 7.9 if bbox_width < 1 else 7

    # plot canton map and municipality data
    fig = px.choropleth_mapbox(
        df_cant,
        geojson=canton_geojson,
        locations="ID_Gemeinde",
        featureidkey="properties.ID_Gemeinde",
        color=data_column,
        color_continuous_scale="Viridis",
        mapbox_style="white-bg",
        zoom=zoom,
        center=center_coords,
        opacity=0.85,
        hover_name="Gemeindename"
    )
    # add dynamic title
    fig.update_layout(
        title=title,
        title_x=0.5,
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        coloraxis_colorbar = {
            "title" : texts.get('title_colorbar'),
            "x": 0.8,
            "xanchor": "left",
            "y" : 0.5,
            "len":0.65,
            "tickformat":"~s"
        }
    )

    # get annotation for the current year and canton
    current_annotation = common.get_current_annotations(annotations, canton, str(year))
    if len(current_annotation):
        fig.update_layout(
            annotations=[
                dict(
                    text=current_annotation,
                    showarrow=False,
                    align="left",
                    xref="paper", yref="paper",
                    x=0.98, y=0.98,
                    bordercolor=gen.colors["purple"],
                    borderwidth=1,
                    borderpad=4,
                    bgcolor=gen.hex_to_rgba_value(gen.colors['purple'], 0.1),
                    opacity=0.9,
                    font=dict(size=12, color="black")
                )
            ]
        )

    return fig

###############################################################################
# setup data
###############################################################################

# read GeoJSON to work locally
with open("./data/Geodaten_Gemeinden_V2.geojson", encoding="utf-8") as f:
    geojson_data = json.load(f)

# get statistical data from file or database
df_csv= pd.read_csv('data/Autodaten_Gemeinden.csv', delimiter=',')

# provide the data as pandas dataframe
df = df_csv.fillna(0)

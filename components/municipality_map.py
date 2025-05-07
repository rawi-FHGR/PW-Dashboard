import dash
import dash_bootstrap_components as dbc

import plotly.express as px
import pandas as pd
import json

# varialbles
texts = {'title':'Fahrzeugbestand pro Gemeinde',
         'title_colorbar':'Anzahl',
         'inhabitant':'Einwohner',
         'stock':'DATA_Bestand',
         'cars':'Personenwagen'}

data_columns = ['DATA_Bestand', 'Gemeindename']

# functions


def generate_map_municipality(year: int, canton: str):
    '''
    Draws a canton outline with municipality data
    :param year:
    :param canton:
    :return: figure object
    '''
    # aggregate municipality data for the given year and canton
    df_cant = (
        df[(df['Kanton'] == canton) & (df['Jahr'] == year)]
        .groupby(['ID_Gemeinde', 'Gemeindename'], as_index=False)
        .agg({'DATA_Bestand': 'sum'})
    )

    # prevent application crash due to missing data
    if df_cant.empty:
        print("Keine Daten für diesen Kanton und Jahr.")
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
    zoom = 9 if bbox_width < 0.5 else 8 if bbox_width < 1 else 7

    # plot canton map and municipality data
    fig = px.choropleth_mapbox(
        df_cant,
        geojson=canton_geojson,
        locations="ID_Gemeinde",
        featureidkey="properties.ID_Gemeinde",
        color="DATA_Bestand",
        color_continuous_scale="Viridis",
        mapbox_style="white-bg",
        zoom=zoom,
        center=center_coords,
        opacity=0.85,
        hover_name="Gemeindename"
    )
    # add dynamic title
    fig.update_layout(
        title=f"<b>{canton}: {texts.get('title')} ({year})</b>",
        title_x=0.5,
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        coloraxis_colorbar = {
            "title" : texts.get('title_colorbar'),
            "x": 0.7,
            "xanchor": "left",
            "y" : 0.5,
            "len":0.65,
            "tickformat":"~s"
        }
    )

    return fig

# setup data
# read simplified GeoJSON to work locally
with open("./data/Geodaten_Gemeinden_V2.geojson", encoding="utf-8") as f:
    geojson_data = json.load(f)

# get statistical data from file or database
df_csv= pd.read_csv('data/Autodaten_Gemeinden.csv', delimiter=',')

# provide the data as pandas dataframe
df = df_csv.fillna(0)

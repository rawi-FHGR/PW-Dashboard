import dash
import dash_bootstrap_components as dbc

import plotly.express as px
import pandas as pd
import json

# setup data
#import helper.setup_data as dat

# definitions
# varialbles
texts = {'title':'Fahrzeugbestand CH',
         'title_colorbar':'Bestand',
         'inhabitant':'Einwohner',
         'stock':'DATA_Bestand',
         'cars':'Personenwagen'}

data_columns = ['DATA_Bestand', 'Gemeindename']

# functions
def generate_map_canton(year: int, canton: str):
    '''
    Draws a canton outline with summarized data (for the canton)
    :param year:
    :param canton:
    :return: figure object
    '''

    # prevent invalid inputs
    if canton not in df['Kanton'].unique():
        # return an empty plot in case of invalid or empty canton selection
        return px.scatter_mapbox()  # Leeres, aber gültiges Objekt

    df_cant = df[(df['Kanton'] == canton) & (df['Jahr'] == year)]

    # inform if no data is available for the current selection
    if df_cant.empty:
        print("Keine Daten für diesen Kanton und Jahr.")
        return px.scatter_mapbox()  # Oder Dummy-Grafik mit Text

    # prepare geojson feature for the selected canton
    features = [
        f for f in geojson_data["features"] if f["properties"]["Kanton"] == canton
    ]
    # ensure not to crash in case of missing features
    if not features:
        return px.scatter_mapbox()

    # calculate the center point of the canton shape
    from shapely.geometry import shape

    geom = shape(features[0]["geometry"])
    #center = geom.centroid
    # bounding box to get minx, miny, maxx, maxy
    minx, miny, maxx, maxy = geom.bounds

    center_coords = {"lat": (miny + maxy) / 2, "lon": (minx + maxx) / 2}

    # rough zoom logic based bbox size (small cantons -> larger zoom)
    bbox_width = maxx - minx
    zoom = 8.5 if bbox_width < 0.5 else 7.5 if bbox_width < 1 else 6.5

    # sum up data for the given canton and year
    df_grouped = df_cant.groupby(['Jahr', 'Kanton'])['DATA_Bestand'].sum().reset_index()

    # draw the map
    fig = px.choropleth_mapbox(
        df_grouped,
        geojson={
            "type": "FeatureCollection",
            "features": [
                f for f in geojson_data["features"] if f["properties"]["Kanton"] == canton
            ]
        },
        locations="Kanton",
        featureidkey="properties.Kanton",
        color="DATA_Bestand",
        color_continuous_scale="Viridis",
        mapbox_style="white-bg",
        center=center_coords,
        zoom=zoom,
        opacity=1.0
    )

    fig.update_layout(
        title=f"<b>Details zu {canton}</b>",
        title_x=0.5,  # centered
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        coloraxis_colorbar=dict(
            title="Bestand",
            x=0.95,  # Rechts positioniert, aber nahe an der Map
            xanchor="left",
            y=0.5,
            len=0.75,  # Vertikale Länge (0–1)
            thickness=15,  # Breite in px
            tickformat="~s"  # z. B. 1k, 10k etc.
        ))
    return fig

# setup data
# read simplified GeoJSON to work locally
with open("./data/Geodaten_Kantone.geojson", encoding="utf-8") as f:
#with open("./data/swiss-cantons.geojson", encoding="utf-8") as f:
    geojson_data = json.load(f)

# get statistical data from file or database
#df = pd.read_csv('./data/bevoelkerung-1990_2024.csv', delimiter=';')
df_csv= pd.read_csv('data/Autodaten_Gemeinden.csv', delimiter=',')
df = df_csv.fillna(0)
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
         'title_colorbar':'Anzahl',
         'inhabitant':'Einwohner',
         'stock':'DATA_Bestand',
         'cars':'Personenwagen'}

data_columns = ['DATA_Bestand', 'Kanton']

# functions
def generate_ch_map(year: int):
    title = f'<b>{texts['title']} {year}</b>'
    data_column = data_columns[0]
    hovertemplate = (
        "<b>%{location}</b><br>"
        "%{z:.0f} " + texts['cars'] + "<br>"
        "<extra></extra>")

    # Filtere das df_ivs auf das gewünschte Jahr
    df_year = df[df['Jahr'] == year]
    # sum car stock per canton
    df_grouped = df_year.groupby(['Jahr', 'Kanton'])['DATA_Bestand'].sum().reset_index()

    # prepare map
    fig = px.choropleth(
        df_grouped,
        geojson=geojson_data,
        locations=data_columns[1],
        featureidkey="properties.NAME_KURZ",
        color=data_column,
        hover_data={data_column: ':.2f'},
        color_continuous_scale="Viridis",
        title=title)

    fig.update_geos(
        fitbounds="locations",
        projection_type="conic conformal",
        visible=False)

    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        # format colorbar
        coloraxis_colorbar={"title": texts['title_colorbar'],
                            "len": 0.5,
                            "x": 0.95,
                            "ticks":"outside",
                            "tickformat":"~s",
                            "xpad": 0,
                            "yanchor": "middle",},
        title_x=0.5,
        title_y=0.97,
        uirevision="constant")

    # get tooltip
    fig.update_traces(hovertemplate=hovertemplate)

    return fig

# setup data
# read simplified GeoJSON to work locally
with open("./data/swiss-cantons.geojson", encoding="utf-8") as f:
    geojson_data = json.load(f)

# get statistical data from file or database
#df = pd.read_csv('./data/bevoelkerung-1990_2024.csv', delimiter=';')
df_csv= pd.read_csv('data/Autodaten_Kantone.csv', delimiter=',')
df = df_csv.fillna(0)
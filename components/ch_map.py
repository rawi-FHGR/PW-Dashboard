import dash
import dash_bootstrap_components as dbc

import plotly.express as px
import pandas as pd
import json

# varialbles
texts = {'title':'Fahrzeugbestand CH',
         'title_colorbar':'Bestand',
         'inhabitant':'Einwohner',
         'stock':'DATA_Bestand',
         'cars':'Personenwagen'}

data_columns = ['DATA_Bestand', 'Kanton']

# functions
def generate_ch_map(year: int):
    '''
    Draws a choropleth map of Switzerland with canton-specific data
    :param year: selected year
    :return: Plotly figure object
    '''

    title = f'<b>{texts['title']} {year}</b>'
    data_column = data_columns[0]

    # get only data for the selected year
    df_year = df[df['Jahr'] == year]

    # 🛑 Check for empty data
    if df_year.empty:
        fig = go.Figure()
        fig.update_layout(
            title=f"<b>Keine Daten für Jahr {year} verfügbar</b>",
            title_x=0.5,
            title_font_size=16,
            margin={"r": 0, "t": 30, "l": 0, "b": 0}
        )
        return fig

    # Daten aggregieren
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
            "title": texts['title_colorbar'],
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

    # tooltip setzen
    hovertemplate = (
        "<b>%{location}</b><br>"
        "%{z:.0f} " + texts['cars'] + "<br>"
        "<extra></extra>"
    )
    fig.update_traces(hovertemplate=hovertemplate)

    return fig

# setup data
# read simplified GeoJSON to work locally
with open("./data/swiss-cantons.geojson", encoding="utf-8") as f:
    geojson_data = json.load(f)

# get statistical data from file or database
df_csv= pd.read_csv('data/Autodaten_Kantone.csv', delimiter=',')

# provide the data as pandas dataframe
df = df_csv.fillna(0)
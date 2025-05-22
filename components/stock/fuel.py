import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash.html as html

import logging

# import project specific settings and functions
import components.common as common

import helper.general as gen
from helper.misc import log_current_function

logger = logging.getLogger(__name__)

# define the texts
texts = {
    'stackedbarchart.title': 'Verteilung Treibstoffarten',
    'relative': 'pro 1000 Einwohner',
    'stackedbarchart.y_axis': 'Anzahl Bestand',
    'piechart.title': 'Anteil Treibstoffarten',
    'infobox.title': 'Bestand nach Treibstoffarten ',
}

# annotation dictionary format: 'year':'message'
annotations = {
    '2016':'Dieselskandal in der<br>Autoindustrie wird publik.',
    '2020':'Corona führt zu einem<br>Rückgang der Inverkehrsetzungen'
}

data_columns = ['Kanton', 'DATA_Bestand', 'DATA_Bestand pro 1000']

def generate_stacked_bar_fuel_stock(df, year, canton, is_relative: bool=False):
    '''
    Generates a stacked bar chart from dataframe with fuel data
    :param df:
    :param year: selected year
    :return: returns a stacked bar chart with fuel data as fig (px.bar)
    '''
    log_current_function(level=logging.DEBUG, msg=f"{year} {canton} {is_relative}")

    # use the right data depending on the data mode
    if is_relative:
        title = f'<b>{canton}: {texts.get("stackedbarchart.title")} {texts.get("relative")} ({year})</b>'
        data_column = data_columns[2]
    else:
        title = f'<b>{canton}: {texts.get("stackedbarchart.title")} ({year})</b>'
        data_column = data_columns[1]

    # only selected canton

    df = df[df['Kanton'] == canton].copy()

    # group data by year and fuel and sum the values
    df_grouped = df.groupby(['Jahr', 'Treibstoff'])[data_column].sum().reset_index()

    # convert year to str
    df_grouped['Jahr'] = df_grouped['Jahr'].astype(int)
    year = int(year)

    # create the stacked bar chart using Plotly Express
    fig = px.bar(df_grouped, x='Jahr',
                 y=data_column,
                 color='Treibstoff',
                 color_discrete_map=common.color_fuel,
                 category_orders={'Jahr': sorted(df_grouped['Jahr'].unique())})

    fig.update_layout(title_text=title,
                      font_size=12,
                      xaxis_title="",
                      yaxis_title=texts.get('stackedbarchart.y_axis'),
                      xaxis={'type': 'category'},
                      )

    # place the legend
    fig.update_layout(
        legend=dict(orientation="h",
                    yanchor="top",
                    y=-0.15,
                    xanchor="center",
                    x=0.5,
                    title=None))

    # add tooltip
    fig.update_traces(
        hovertemplate=(
                "Jahr: %{x}<br>" +
                "Treibstoff: %{fullData.name}<br>" +
                "%{y:.0f} Personenwagen<br>" +
                "<extra></extra>"))

    # group by year and sum up the values (Anzahl)
    yearly_sum = df_grouped.groupby('Jahr')[data_column].sum()

    # get the max value for the sum
    max_sum = yearly_sum.max()

    # get, if there are, annotation texts for the selected year
    annotation_text = annotations.get(str(year)) if annotations else None
    common.add_year_marker(fig, year, max_sum, color=gen.colors['purple'], annotation=annotation_text)

    return fig

def generate_pie_fuel_stock(df, year, canton, is_relative: bool=False):
    log_current_function(level=logging.DEBUG, msg=f"{year} {canton} {is_relative}")
    
    # Pro Jahr filtern, ansonsten Summe über alle Jahre!
    df = df[(df['Jahr'] == year) & (df['Kanton'] == canton)].copy()
    
    # use the right data depending on the data mode
    if is_relative:
        title = f'<b>{canton}: {texts.get("piechart.title")} {texts.get("relative")} ({year})</b>'
        data_column = data_columns[2]
    else:
        title = f'<b>{canton}: {texts.get("piechart.title")} ({year})</b>'
        data_column = data_columns[1]


    # group data by year and fuel and sum the values
    df_grouped = df.groupby(['Treibstoff'])[data_column].sum().reset_index()
    df_grouped['Jahr'] = year # needed for the tooltip

    # set chart parameters
    labels = df_grouped["Treibstoff"]
    values = df_grouped[data_column]
    customdata = [[year]] * len(df_grouped)
    colors = [common.color_fuel.get(label, "#cccccc") for label in labels]

    # piechart with hovertemplate
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                customdata=customdata,
                textinfo='percent+label',
                textposition='inside',
                marker=dict(colors=colors),
                hovertemplate=(
                    "Jahr: %{customdata[0]}<br>"
                    "Treibstoff: %{label}<br>"
                    "%{value:.0f} Personenwagen<br>"
                    "<extra></extra>"
                ),
                showlegend=False
            )
        ]
    )

    fig.update_layout(
        title=title,
        margin=dict(t=52)
    )

    return fig

def generate_fuel_summary_text(df, year, canton, is_relative: bool=False):
    log_current_function(level=logging.DEBUG, msg=f"{year} {canton} {is_relative}")

    # use the right data depending on the data mode
    if is_relative:
        title = f'{canton}: {texts.get("infobox.title")} {texts.get("relative")} ({year})'
        data_column = data_columns[2]
    else:
        title = f'{canton}: {texts.get("infobox.title")} ({year})'
        data_column = data_columns[1]

    # only selected canton
    df = df[(df['Jahr'] == year) & (df['Kanton'] == canton)].copy()

    # group and sort the car stock
    df_grouped = df.groupby('Treibstoff')[data_column].sum().reset_index()
    df_grouped = df_grouped.sort_values(by=data_column, ascending=False)

    # calculate total
    total = df_grouped[data_column].sum()

    # content of the infobox
    text_block = [
        html.P(f"{title}", style={**common.text_style, 'fontWeight': 'bold', 'marginTop': '0px', 'fontSize': '0.95vw'}),
        html.Ul([
            html.Li(
                f"{row['Treibstoff']}: {int(row[data_column]):,}".replace(',', "'"),
                style=common.text_style
            )
            for _, row in df_grouped.iterrows()
        ]),
        html.P(
            f"Total: {int(total):,}".replace(',', "'"),
            style={**common.text_style, 'fontWeight': 'bold', 'marginTop': '10px'}
        )
    ]

    return html.Div(text_block, style={
        'padding': '0px',
        'border': 'none',
        'backgroundColor': 'transparent'
    })

#################################################
### get and setup data
#################################################
df_csv= pd.read_csv('data/Autodaten_Kantone.csv', delimiter=',')
df_fuel = df_csv.fillna(0)
df_fuel = gen.normalize_fuel_categories(df_fuel)
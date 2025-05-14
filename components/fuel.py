import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import logging

# import project specific settings and functions
import helper.general as gen
from helper.misc import log_current_function

logger = logging.getLogger(__name__)

color_fuel= {
    "Benzin": gen.colors['blue'],
    "Diesel": gen.colors['orange'],
    "Hybrid": gen.colors['green'],
    "Elektrisch": gen.colors['red'],
    "Andere": gen.colors['purple'],
    "Gas": gen.colors['brown'],
    "Wasserstoff": gen.colors['grey']
}

data_columns = ['Gemeindename', 'DATA_Bestand', 'DATA_Bestand pro 1000']

def generate_stacked_bar_fuel_ivs(df, jahr):
    '''
    WORK IN PROGRESS!
    Generates a stacked bar chart from dataframe with fuel data
    :param df:
    :param jahr: selected year
    :return: returns a stacked bar chart with fuel data as fig (px.bar)
    '''

    # group data by year and fuel and sum the values
    df_grouped = df.groupby(['Jahr', 'Treibstoff'])['DATA_Inverkehrsetzung'].sum().reset_index()

    # Create the stacked bar chart using Plotly Express
    fig = px.bar(df_grouped, x='Jahr', y='DATA_Inverkehrsetzung', color='Treibstoff', color_discrete_map=color_fuel)
    fig.update_layout(title_text=f"<b>Verteilung der Treibstoffarten</b>",
                      font_size=12,
                      xaxis_title="",
                      yaxis_title="Anzahl Inverkehrsetzungen")

    fig.update_layout(xaxis={'type': 'category'})

    # # group by year and sum up the values (Anzahl)
    # yearly_sum = df.groupby('Jahr')['Anzahl'].sum()
    #
    # # get the max value for the sum
    # max_sum = yearly_sum[yearly_sum.idxmax()]

    # place the legend
    fig.update_layout(
        legend=dict(orientation="h",
                    yanchor="top",
                    y=-0.05,
                    xanchor="center",
                    x=0.5,
                    title=None))

    # # add a red line to indicate the selected year
    # fig.add_shape(type="line",
    #               x0=jahr, y0=0,
    #               x1=jahr, y1=int(max_sum),
    #               line=dict(color=gen.colors['rot'], width=3))
    #
    # # add a red circle on the x-axis to indicate the selected year
    # fig.add_trace(go.Scatter(x=[jahr], y=[0], mode='markers',
    #                          marker=dict(color='Red', size=10, symbol='circle'),
    #                 showlegend=False))
    return fig

def generate_stacked_bar_fuel_stock(df, year, is_relative: bool=False):
    '''
    Generates a stacked bar chart from dataframe with fuel data.
    The selected year is emphasized with a colored marker
    :param df:
    :param year: selected year
    :return: returns a stacked bar chart with fuel data as fig (px.bar)
    '''
    log_current_function(level=logging.DEBUG, msg=f"{year} {is_relative}")

    texts = {'title': 'Verteilung der Treibstoffarten CH',
             'title_colorbar': 'Anzahl',
             'inhabitant': 'Einwohner',
             'stock': 'DATA_Bestand',
             'cars': 'Personenwagen'}

    # use the right data depending on the data mode
    if is_relative:
        title = f'<b>{texts.get('title')} pro 1000 Einwohner ({year})</b>'
        data_column = data_columns[2]
    else:
        title = f'<b>{texts.get('title')} ({year})</b>'
        data_column = data_columns[1]

    # group data by year and fuel and sum the values
    df_grouped = df.groupby(['Jahr', 'Treibstoff'])[data_column].sum().reset_index()

    # create the stacked bar chart using Plotly Express
    fig = px.bar(df_grouped, x='Jahr', y=data_column, color='Treibstoff', color_discrete_map=color_fuel)
    fig.update_layout(title_text=title,
                      font_size=12,
                      xaxis_title="",
                      yaxis_title="Anzahl Bestand")

    fig.update_layout(xaxis={'type': 'category'})

    # # group by year and sum up the values (Anzahl)
    yearly_sum = df_grouped.groupby('Jahr')[data_column].sum()
    # get the max value for the sum
    max_sum = yearly_sum.max()

    # place the legend
    fig.update_layout(
        legend=dict(orientation="h",
                    yanchor="top",
                    y=-0.05,
                    xanchor="center",
                    x=0.5,
                    title=None))

    # add year marker
    add_year_marker(fig, year, max_sum, color=gen.colors['red'])

    return fig

def generate_stacked_bar_fuel_stock_canton(df, year, canton, is_relative: bool=False):
    '''
    Generates a stacked bar chart from dataframe with fuel data
    :param df:
    :param year: selected year
    :return: returns a stacked bar chart with fuel data as fig (px.bar)
    '''
    log_current_function(level=logging.DEBUG, msg=f"{year} {canton} {is_relative}")

    texts = {'title': 'Fahrzeugbestand',
             'title_colorbar': 'Anzahl',
             'inhabitant': 'Einwohner',
             'stock': 'DATA_Bestand',
             'cars': 'Personenwagen'}

    # use the right data depending on the data mode
    if is_relative:
        title = f'<b>{canton}: {texts.get('title')} pro 1000 Einwohner ({year})</b>'
        data_column = data_columns[2]
    else:
        title = f'<b>{canton}: {texts.get('title')} ({year})</b>'
        data_column = data_columns[1]

    # only selected canton
    df_canton = df[df['Kanton'] == canton].copy()

    # group data by year and fuel and sum the values
    df_grouped = df_canton.groupby(['Jahr', 'Treibstoff'])[data_column].sum().reset_index()

    # convert year to str
    df_grouped['Jahr'] = df_grouped['Jahr'].astype(int)
    year = int(year)

    # create the stacked bar chart using Plotly Express
    fig = px.bar(df_grouped, x='Jahr',
                 y=data_column,
                 color='Treibstoff',
                 color_discrete_map=color_fuel,
                 category_orders={'Jahr': sorted(df_grouped['Jahr'].unique())})

    fig.update_layout(title_text=title,
                      font_size=12,
                      xaxis_title="",
                      yaxis_title="Anzahl Bestand",
                      xaxis={'type': 'category'})

    # place the legend
    fig.update_layout(
        legend=dict(orientation="h",
                    yanchor="top",
                    y=-0.05,
                    xanchor="center",
                    x=0.5,
                    title=None)
    )

    # group by year and sum up the values (Anzahl)
    yearly_sum = df_grouped.groupby('Jahr')[data_column].sum()

    # get the max value for the sum
    max_sum = yearly_sum.max()

    # add year marker
    add_year_marker(fig, year, max_sum, color=gen.colors['red'])

    return fig

def generate_multiline_total(df, jahr):
    '''
    WORK IN PROGRESS!
    Generates a stacked bar chart from dataframe with fuel data
    :param df:
    :param jahr: selected year
    :return: returns a stacked bar chart with fuel data as fig (px.bar)
    '''

    # group data by year and sum the values for both ivs (Inverkehrsezung) and stock (Bestand)
    df_grouped = df.groupby('Jahr')[['DATA_Inverkehrsetzung', 'DATA_Bestand']].sum().reset_index()

    fig = go.Figure()

    # positioning of the text label
    last_x = df_grouped['Jahr'].iloc[-1]
    label_x = last_x - 0.5

    # line 1: ivs (Inverkehrsetzungen)
    fig.add_trace(go.Scatter(
        x=df_grouped['Jahr'],
        y=df_grouped['DATA_Inverkehrsetzung'],
        mode='lines+text',
        line=dict(color='blue'),
        text=[""] * (len(df_grouped) - 1) + ['Inverkehrsetzungen'],
        textposition='top left',
        textfont=dict(color='blue'),
        showlegend=False
    ))

    # Line 2: stock (Bestand)
    fig.add_trace(go.Scatter(
        x=df_grouped['Jahr'],
        y=df_grouped['DATA_Bestand'],
        mode='lines+text',
        line=dict(color='green'),
        text=[""] * (len(df_grouped) - 1) + ['Bestand'],
        textposition='top left',
        textfont=dict(color='green'),
        showlegend=False
    ))

    # add title and axis labels
    fig.update_layout(
        title='<b>Inverkehrsetzungen und Fahrzeugbestand pro Jahr</b>',
        font_size=12,
        xaxis_title='Jahr',
        yaxis_title='Anzahl Fahrzeuge',
        margin=dict(l=40, r=20, t=40, b=40)
    )

    return fig

def generate_pie_fuel_stock(df_jahr, year, is_relative: bool=False):
    log_current_function(level=logging.DEBUG, msg=f"{year} {is_relative}")

    texts = {'title': 'Anteil Treibstoffarten CH',
             'title_colorbar': 'Anzahl',
             'inhabitant': 'Einwohner',
             'stock': 'DATA_Bestand',
             'cars': 'Personenwagen'}

    # use the right data depending on the data mode
    if is_relative:
        title = f'<b>{texts.get('title')} pro 1000 Einwohner ({year})</b>'
        data_column = data_columns[2]
    else:
        title = f'<b>{texts.get('title')} ({year})</b>'
        data_column = data_columns[1]

    df_grouped = df_jahr.groupby(['Jahr', 'Treibstoff'])[data_column].sum().reset_index()

    fig = px.pie(
        df_grouped,
        names="Treibstoff",
        values=data_column,
        title=title,
        color="Treibstoff",
        color_discrete_map=color_fuel
    )
    fig.update_layout(margin=dict(t=52))
    fig.update_traces(textposition='inside', textinfo='percent+label', showlegend=False )
    return fig

def generate_pie_fuel_stock_canton(df, year, canton, is_relative: bool=False):
    log_current_function(level=logging.DEBUG, msg=f"{year} {canton} {is_relative}")

    texts = {'title': 'Anteil Treibstoffarten',
             'title_colorbar': 'Anzahl',
             'inhabitant': 'Einwohner',
             'stock': 'DATA_Bestand',
             'cars': 'Personenwagen'}

    # use the right data depending on the data mode
    if is_relative:
        title = f'<b>{canton}: {texts.get('title')} pro 1000 Einwohner ({year})</b>'
        data_column = data_columns[2]
    else:
        title = f'<b>{canton}: {texts.get('title')} ({year})</b>'
        data_column = data_columns[1]

    df_canton = df[df['Kanton'] == canton]

    # group data by year and fuel and sum the values
    df_grouped = df_canton.groupby(['Jahr', 'Treibstoff'])[data_column].sum().reset_index()

    fig = px.pie(
        df_grouped,
        names="Treibstoff",
        values=data_column,
        title=title,
        color="Treibstoff",
        color_discrete_map=color_fuel
    )
    fig.update_layout(margin=dict(t=52))
    fig.update_traces(textposition='inside', textinfo='percent+label', showlegend=False )
    return fig


def generate_fuel_summary_text_CH(df, year, is_relative: bool=False):
    log_current_function(level=logging.DEBUG, msg=f"{year} {is_relative}")

    import dash.html as html

    texts = {'title': 'Bestand nach Treibstoffarten CH',
             'title_colorbar': 'Anzahl',
             'inhabitant': 'Einwohner',
             'stock': 'DATA_Bestand',
             'cars': 'Personenwagen'}

    # use the right data depending on the data mode
    if is_relative:
        title = f'{texts.get('title')} pro 1000 Einwohner ({year})'
        data_column = data_columns[2]
    else:
        title = f'{texts.get('title')} ({year})'
        data_column = data_columns[1]

    # Filterung
    df_canton = df[(df['Jahr'] == year)]

    # Gruppierung und Sortierung nach DATA_Bestand (absteigend)
    df_grouped = df_canton.groupby('Treibstoff')[data_column].sum().reset_index()
    df_grouped = df_grouped.sort_values(by=data_column, ascending=False)

    # Gesamttotal berechnen
    total = df_grouped[data_column].sum()

    # Einheitlicher Textstil (analog Plotly)
    text_style = {
        'fontFamily': 'Arial, sans-serif',  # oder die gleiche wie in deinem Plotly-Layout
        'fontSize': '18px',
        'color': '#000000'
    }

    # Inhalt der Textbox
    text_block = [
        html.P(f"{title}", style={**text_style, 'fontWeight': 'bold', 'marginTop': '10px', 'fontSize': '20px'}),
        html.Ul([
            html.Li(
                f"{row['Treibstoff']}: {int(row[data_column]):,}".replace(',', "'"),
                style=text_style
            )
            for _, row in df_grouped.iterrows()
        ]),
        html.P(
            f"Total: {int(total):,}".replace(',', "'"),
            style={**text_style, 'fontWeight': 'bold', 'marginTop': '10px'}
        )
    ]

    return html.Div(text_block, style={
        'padding': '0px',  # kein Innenabstand nötig
        'border': 'none',  # keine Umrandung
        'backgroundColor': 'transparent'
    })


def generate_fuel_summary_text_canton(df, year, canton, is_relative: bool=False):
    log_current_function(level=logging.DEBUG, msg=f"{year} {canton} {is_relative}")

    import dash.html as html

    texts = {'title': 'Bestand nach Treibstoffarten ',
             'title_colorbar': 'Anzahl',
             'inhabitant': 'Einwohner',
             'stock': 'DATA_Bestand',
             'cars': 'Personenwagen'}

    # use the right data depending on the data mode
    if is_relative:
        title = f'{canton}: {texts.get('title')} pro 1000 Einwohner ({year})'
        data_column = data_columns[2]
    else:
        title = f'{canton}: {texts.get('title')} ({year})'
        data_column = data_columns[1]

    # Filterung
    df_canton = df[(df['Kanton'] == canton) & (df['Jahr'] == year)]

    # Gruppierung und Sortierung nach DATA_Bestand (absteigend)
    df_grouped = df_canton.groupby('Treibstoff')[data_column].sum().reset_index()
    df_grouped = df_grouped.sort_values(by=data_column, ascending=False)

    # Gesamttotal berechnen
    total = df_grouped[data_column].sum()

    # Einheitlicher Textstil (analog Plotly)
    text_style = {
        'fontFamily': 'Arial, sans-serif',  # oder die gleiche wie in deinem Plotly-Layout
        'fontSize': '18px',
        'color': '#000000'
    }

    # Inhalt der Textbox
    text_block = [
        html.P(f"{title}", style={**text_style, 'fontWeight': 'bold', 'marginTop': '10px', 'fontSize': '20px'}),
        html.Ul([
            html.Li(
                f"{row['Treibstoff']}: {int(row[data_column]):,}".replace(',', "'"),
                style=text_style
            )
            for _, row in df_grouped.iterrows()
        ]),
        html.P(
            f"Total: {int(total):,}".replace(',', "'"),
            style={**text_style, 'fontWeight': 'bold', 'marginTop': '10px'}
        )
    ]

    return html.Div(text_block, style={
        'padding': '0px',  # kein Innenabstand nötig
        'border': 'none',  # keine Umrandung
        'backgroundColor': 'transparent'
    })


#################################################
### helper functions
#################################################
def add_year_marker(figure, year, y_max, color='red'):
    """
    Adds a vertical marker (line and point) to a chart (given as figure object).
    Works also with categorical x-axis (strings).

    :param figure: Plotly figure object (e.g. px.bar)
    :param year: year, which will be marked (int or str)
    :param y_max: max y-size (for the vertical line)
    :param color: color of the marker
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

#################################################
### get and setup data
#################################################
df_csv= pd.read_csv('data/Autodaten_Kantone.csv', delimiter=',')
df_fuel = df_csv.fillna(0)
df_fuel = gen.normalize_fuel_categories(df_fuel)

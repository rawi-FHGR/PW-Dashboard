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

# define the texts
texts = {
    'stackedbarchart.title': 'Verteilung der Treibstoffarten',
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
    if canton != 'CH':
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
                 color_discrete_map=color_fuel,
                 category_orders={'Jahr': sorted(df_grouped['Jahr'].unique())})

    fig.update_layout(title_text=title,
                      font_size=12,
                      xaxis_title="",
                      yaxis_title=texts.get('stackedbarchart.y_axis'),
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

    # get, if there are, annotation texts for the selected year
    annotation_text = annotations.get(str(year)) if annotations else None
    add_year_marker(fig, year, max_sum, color=gen.colors['red'], annotation=annotation_text)

    return fig

def generate_pie_fuel_stock(df, year, canton, is_relative: bool=False):
    log_current_function(level=logging.DEBUG, msg=f"{year} {canton} {is_relative}")
    
    # Pro Jahr filtern, ansonsten Summe über alle Jahre!
    df = df[df['Jahr'] == year].copy()
    
    # use the right data depending on the data mode
    if is_relative:
        title = f'<b>{canton}: {texts.get("piechart.title")} {texts.get("relative")} ({year})</b>'
        data_column = data_columns[2]
    else:
        title = f'<b>{canton}: {texts.get("piechart.title")} ({year})</b>'
        data_column = data_columns[1]
    
    # only selected canton
    if canton != 'CH':
      df = df[df['Kanton'] == canton].copy()

    # group data by year and fuel and sum the values
    df_grouped = df.groupby(['Treibstoff'])[data_column].sum().reset_index()

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



def generate_fuel_summary_text(df, year, canton, is_relative: bool=False):
    log_current_function(level=logging.DEBUG, msg=f"{year} {canton} {is_relative}")

    import dash.html as html

    # use the right data depending on the data mode
    if is_relative:
        title = f'{canton}: {texts.get("infobox.title")} {texts.get("relative")} ({year})'
        data_column = data_columns[2]
    else:
        title = f'{canton}: {texts.get("infobox.title")} ({year})'
        data_column = data_columns[1]

    # only selected canton
    if canton != 'CH':
        df = df[(df['Kanton'] == canton) & (df['Jahr'] == year)].copy()


    
    # Gruppierung und Sortierung nach DATA_Bestand (absteigend)
    df_grouped = df.groupby('Treibstoff')[data_column].sum().reset_index()
    df_grouped = df_grouped.sort_values(by=data_column, ascending=False)

    # calculate total
    total = df_grouped[data_column].sum()

    # uniform text style
    text_style = {
        'fontFamily': 'Arial, sans-serif',  # oder die gleiche wie in deinem Plotly-Layout
        'fontSize': '18px',
        'color': '#000000'
    }

    # content of the infobox
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
        'padding': '0px',
        'border': 'none',
        'backgroundColor': 'transparent'
    })

#################################################
### helper functions
#################################################
def add_year_marker(figure, year, y_max, color='red', annotation: str=''):
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
            bgcolor=gen.hex_to_rgba_value(color, 0.1),    # or: white
            bordercolor=color,
            borderwidth=1,
            align='center'
        )


#################################################
### get and setup data
#################################################
df_csv= pd.read_csv('data/Autodaten_Kantone.csv', delimiter=',')
df_fuel = df_csv.fillna(0)
df_fuel = gen.normalize_fuel_categories(df_fuel)

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# import project specific settings and functions
import helper.general as gen

# get statistical data from cvs files
# carbody data (Karosserie)
df_csv= pd.read_csv('data/Autodaten_Kantone.csv', delimiter=',')
df_fuel = df_csv.fillna(0)

farben_fuel = {
    "Benzin": gen.colors['blue'],
    "Diesel": gen.colors['orange'],
    "Hybrid": gen.colors['green'],
    "Elektrisch": gen.colors['red'],
    "Wasserstoff": gen.colors['purple'],
    "Gas": gen.colors['brown'],
    "andere": gen.colors['grey']
}

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
    fig = px.bar(df_grouped, x='Jahr', y='DATA_Inverkehrsetzung', color='Treibstoff', color_discrete_map=farben_fuel)
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


def generate_stacked_bar_fuel_stock(df, jahr):
    '''
    WORK IN PROGRESS!
    Generates a stacked bar chart from dataframe with fuel data
    :param df:
    :param jahr: selected year
    :return: returns a stacked bar chart with fuel data as fig (px.bar)
    '''

    # group data by year and fuel and sum the values
    df_grouped = df.groupby(['Jahr', 'Treibstoff'])['DATA_Bestand'].sum().reset_index()

    # create the stacked bar chart using Plotly Express
    fig = px.bar(df_grouped, x='Jahr', y='DATA_Bestand', color='Treibstoff', color_discrete_map=farben_fuel)
    fig.update_layout(title_text=f"<b>Verteilung der Treibstoffarten (CH)</b>",
                      font_size=12,
                      xaxis_title="",
                      yaxis_title="Anzahl Bestand")

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

def generate_stacked_bar_fuel_stock_canton(df, jahr, canton):
    '''
    WORK IN PROGRESS!
    Generates a stacked bar chart from dataframe with fuel data
    :param df:
    :param jahr: selected year
    :return: returns a stacked bar chart with fuel data as fig (px.bar)
    '''

    df_canton = df[df['Kanton'] == canton]

    # group data by year and fuel and sum the values
    df_grouped = df_canton.groupby(['Jahr', 'Treibstoff'])['DATA_Bestand'].sum().reset_index()

    # create the stacked bar chart using Plotly Express
    fig = px.bar(df_grouped, x='Jahr', y='DATA_Bestand', color='Treibstoff', color_discrete_map=farben_fuel)
    fig.update_layout(title_text=f"<b>Verteilung der Treibstoffarten {canton}</b>",
                      font_size=12,
                      xaxis_title="",
                      yaxis_title="Anzahl Bestand")

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

def generate_pie_fuel_stock(df_jahr, jahr):
    df_grouped = df_jahr.groupby(['Jahr', 'Treibstoff'])['DATA_Bestand'].sum().reset_index()

    fig = px.pie(
        df_grouped,
        names="Treibstoff",
        values="DATA_Bestand",
        title=f"<b>Anteil Treibstoffarten CH ({jahr})</b>",
        color="Treibstoff",
        color_discrete_map=farben_fuel
    )
    fig.update_layout(margin=dict(t=52))
    fig.update_traces(textposition='inside', textinfo='percent+label', showlegend=False )
    return fig

def generate_pie_fuel_stock_canton(df, jahr, canton):

    df_canton = df[df['Kanton'] == canton]

    # group data by year and fuel and sum the values
    df_grouped = df_canton.groupby(['Jahr', 'Treibstoff'])['DATA_Bestand'].sum().reset_index()

    fig = px.pie(
        df_grouped,
        names="Treibstoff",
        values="DATA_Bestand",
        title=f"<b>Anteil Treibstoffarten {canton} ({jahr})</b>",
        color="Treibstoff",
        color_discrete_map=farben_fuel
    )
    fig.update_layout(margin=dict(t=52))
    fig.update_traces(textposition='inside', textinfo='percent+label', showlegend=False )
    return fig
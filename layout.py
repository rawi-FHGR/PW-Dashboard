import dash.html as html
import dash.dcc as dcc

from helper.general import available_years, default_year
from components.canton_map import generate_map_canton

# variables
texts = {'page.title':'Personenwagen-Dashboard',
         'title_colorbar':'Anzahl'}

# functions
def create_layout():
        return html.Div([
    html.H1(texts['page.title'], style={'textAlign': 'center'}),

    # Wrapper für Karten: Zeilenlayout
    html.Div([
        dcc.Graph(id='choropleth-map', style={'width': '40%'}),
        html.Div(id='selected-canton-output', style={
            'width': '30%',
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center',
            'fontSize': '24px',
            'fontWeight': 'bold'
        }),
        dcc.Graph(id='choropleth-map-canton', figure=generate_map_canton(2023, 'ZH'), style={'width': '30%'})
    ], style={
        'display': 'flex',
        'flexDirection': 'row',  # nebeneinander
        'width': '100%',
        'gap': '10px',
        'justifyContent': 'center',
        'alignItems': 'stretch',
        'marginBottom': '20px'
    }),

    # Year Slider
    html.Div(
        dcc.Slider(
            id='year-slider',
            min=int(min(available_years)),
            max=int(max(available_years)),
            step=1,
            value=int(default_year),
            marks={
                int(min(available_years)): str(int(min(available_years))),
                int(max(available_years)): str(int(max(available_years)))
            },
            tooltip={"placement": "bottom", "always_visible": True},
            className='custom-slider'
        ),
        style={'width': '25%', 'margin': '20px auto'}
    ),

    # Weitere Grafiken unten
    html.Div([
        html.Div(dcc.Graph(id='stackedbar-fuel-ivs', style={'height': '100%'}), style={'width': '33%'}),
        html.Div(dcc.Graph(id='stackedbar-fuel-stock', style={'height': '100%'}), style={'width': '33%'}),
        html.Div(dcc.Graph(id='multiline-total', style={'height': '100%'}), style={'width': '33%'})
    ], style={
        'display': 'flex',
        'flexDirection': 'row',
        'justifyContent': 'space-between',
        'alignItems': 'stretch',
        'width': '100%',
        'gap': '10px',
        'padding': '10px'
    })
])

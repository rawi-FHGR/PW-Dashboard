import dash.html as html
import dash.dcc as dcc

from components.municipality_map import generate_map_municipality
from helper.general import available_years, default_year
from components.canton_map import generate_map_canton

# keep texts centralized
texts = {'page.title':'Personenwagen-Dashboard',
         'title_colorbar':'Anzahl'}

# functions
def create_layout():
        return html.Div([
            dcc.Tabs([
            dcc.Tab(label='Bestand', children=[
            html.H1(texts['page.title'], style={'textAlign': 'center'}),

            # 1st line: CH map and canton / municipality map
            html.Div([
                dcc.Graph(id='choropleth-map', style={'width': '50%', 'border': '1px solid black','boxSizing': 'border-box','border-radius': '25px','overflow': 'hidden'}),
                dcc.Graph(id='choropleth-map-municipality',
                          figure=generate_map_municipality(2023, 'ZH'), style={'width': '50%', 'border': '1px solid black','boxSizing': 'border-box','border-radius': '25px','overflow': 'hidden'})
            ], style={
                'display': 'flex',
                'flexDirection': 'row',  # nebeneinander
                'width': '100%',
                'gap': '10px',
                'justifyContent': 'center',
                'alignItems': 'stretch',
                'marginBottom': '20px'
            }),

            # 2nd line: year slider
            html.Div(
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
                style={'width': '50%', 'margin': '20px auto'}
            ),
        style={'background-color': 'white','border': '1px solid black','boxSizing': 'border-box','border-radius': '25px','overflow': 'hidden'}),

            # additional graphs (3 side-by-side)
            html.Div([
                html.Div(dcc.Graph(id='stackedbar-fuel-ivs', style={'height': '100%'}), style={'width': '33.333%','border': '1px solid black','boxSizing': 'border-box','border-radius': '25px','overflow': 'hidden'}),
                html.Div(dcc.Graph(id='stackedbar-fuel-stock', style={'height': '100%'}), style={'width': '33.333%','border': '1px solid black','boxSizing': 'border-box','border-radius': '25px','overflow': 'hidden'}),
                html.Div(dcc.Graph(id='multiline-total', style={'height': '100%'}), style={'width': '33.333%','border': '1px solid black','boxSizing': 'border-box','border-radius': '25px','overflow': 'hidden'})
            ], style={
                'display': 'flex',
                'flexDirection': 'row',
                'justifyContent': 'space-between',
                'alignItems': 'stretch',
                'width': '100%',
                'gap': '10px',
                'padding-top': '10px'

            })
        ],
                    style={
                        'padding': '12px',
                        'fontSize': '18px',
                        'fontWeight': 'bold',
                        'backgroundColor': 'white',
                        'color': 'black',
                        'border': '2px solid black',
                        'border-radius-top-right':'50px',
                        'border-top-right-radius': '50px',
                    },
                    selected_style={
                        'padding': '12px',
                        'fontSize': '18px',
                        'fontWeight': 'bold',
                        'backgroundColor': 'red',
                        'color': 'black',
                        'border': '2px solid black',
                        'borderBottom': 'none',
                        'border-top-right-radius':'50px',
                    }
                    ),
        dcc.Tab(label='Inverkehrssetzungen', children=[
            html.Div("andere Inhalte", style={'padding':'20px'})
            ]
                ,
                style={
                    'padding': '12px',
                        'fontSize': '18px',
                        'fontWeight': 'bold',
                        'backgroundColor': 'white',
                        'color': 'black',
                        'border': '2px solid black',
                        'border-radius-top-right':'50px',
                        'border-top-left-radius': '50px',
                },
                selected_style={
                    'padding': '12px',
                    'fontSize': '18px',
                    'fontWeight': 'bold',
                    'backgroundColor': 'red',
                    'color': 'black',
                    'border': '2px solid black',
                    'borderBottom': 'none',
                    'border-top-right-radius':'50px',
                }
                ,
                )
            ])
            ], style={'backgroundColor': 'red'}
        )

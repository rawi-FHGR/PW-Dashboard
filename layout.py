import dash.html as html
import dash.dcc as dcc
import dash_daq as daq
from click import style

from helper.general import available_years, default_year

# initialize logger
import logging
from helper.misc import log_current_function
logger = logging.getLogger(__name__)

# keep texts centralized
texts = {'page.title':'Personenwagen-Dashboard',
         'title_colorbar':'Anzahl'}

# functions
def create_layout():
    log_current_function(level=logging.INFO, msg=f"{__name__}")
    return html.Div([
        dcc.Tabs([
            dcc.Tab(
                label='Bestand',
                children=[
                   #html.H1(texts['page.title'], style={'textAlign': 'center'}),

                    # Header mit Titel + Schweizerwappen
                    html.Div([
                        html.Div(style={'width': '33%'}), #Platz für Logo etc.
                        html.H1("Personenwagen-Dashboard", style={'margin': 0}),
                        html.Div(style={'width': '33%'}),  # Platz für Logo etc.
                    ], style={
                        'display': 'flex',
                        'justifyContent': 'space-between',
                        'alignItems': 'center',
                        'padding': '10px 20px'
                    }),

                    # 1st line: CH map and canton / municipality map
                    html.Div([
                        dcc.Graph(id='choropleth-map', style={
                            'width': '67%',
                            'border': '1px solid black',
                            'border-radius': '10px',
                            'overflow': 'hidden',
                            'margin-left': '10px'
                        }),
                        html.Div(id='right-panel', style={
                            'width': '33%',
                            'border': '1px solid black',
                            'border-radius': '10px',
                            'overflow': 'hidden',
                            'margin-right': '10px',
                            'background-color':'white',
                            'padding': '10px'
                        })
                    ], style={
                        'display': 'flex',
                        'flexDirection': 'row',
                        'width': '100%',
                        'gap': '10px',
                        'justifyContent': 'center',
                        'alignItems': 'stretch',
                        'marginBottom': '20px',
                        'height': '450px'
                    }),

                    # 2nd line: Home-Button, year slider + toggle
                    html.Div([
                        html.Div(
                            html.Img(
                                id="home-button",
                                src="/assets/swisscoat.png",
                                title="Zur Ausgangsansicht zurückkehren",
                                n_clicks=0,
                                style={
                                    'height': '40px',
                                    'cursor': 'pointer',
                                    'marginRight': '20px',
                                }
                            ),style={'width': '10%', 'display': 'flex', 'justifyContent': 'center'},
                        ),
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
                            style={'width': '60%'}
                        ),
                        html.Div(
                            daq.ToggleSwitch(
                                id='value-mode-toggle',
                                label='Relativ',
                                labelPosition='top',
                                value=True
                            ),
                            style={'width': '10%', 'textAlign': 'center','justifyContent': 'center','display':'flex'}
                        ),
                    ], style={
                        'display': 'flex',
                        'flexDirection': 'row',
                        'alignItems': 'center',
                        'justifyContent': 'space-between',
                        'width': 'auto',
                        'margin': '10px',
                        'padding': '10px',
                        'background-color':'white',
                        'border': '1px solid black',
                        'border-radius': '10px',
                        'overflow': 'hidden',
                        'gap': '10px',
                    }),

                    # additional graphs (3 side-by-side)
                    html.Div([
                        html.Div(dcc.Graph(id='stackedbar-fuel-stock-canton', style={'height': '100%'}), style={'width': '33%','border': '1px solid black',
                                'boxSizing': 'border-box',
                                'border-radius': '25px',
                                'overflow': 'hidden'}),
                        html.Div(dcc.Graph(id='pie-fuel-stock', style={'height': '100%'}), style={'width': '33%','border': '1px solid black',
                                'boxSizing': 'border-box',
                                'border-radius': '25px',
                                'overflow': 'hidden'}),
                        html.Div(id='summary-container', style={'width': '33%','border': '1px solid black',
                                'boxSizing': 'border-box',
                                'border-radius': '25px',
                                'overflow': 'hidden',
                                'backgroundColor': 'white',
                                'padding': '10px',})
                    ], style={
                        'display': 'flex',
                        'flexDirection': 'row',
                        'justifyContent': 'space-between',
                        'alignItems': 'stretch',
                        'width': '100%',
                        'gap': '10px',
                        'padding': '10px',
                        'height': '325px'
                    }),

                    # define stores (callback chaining)
                    html.Div([
                        dcc.Store(id="selected-canton", data="CH"),
                        dcc.Store(id="selected-municipality")
                    ], id="hidden-stores", style={"display": "none"})
                ],
                # style of the tabs
                style={
                    'padding': '12px',
                    'fontSize': '18px',
                    'fontWeight': 'bold',
                    'backgroundColor': 'white',
                    'color': 'black',
                    'border': '2px solid black',
                    'border-top-right-radius': '50px'
                },
                selected_style={
                    'padding': '12px',
                    'fontSize': '18px',
                    'fontWeight': 'bold',
                    'backgroundColor': 'red',
                    'color': 'black',
                    'border': '2px solid black',
                    'borderBottom': 'none',
                    'border-top-right-radius': '50px'
                }
            ),
            # second tab
            dcc.Tab(
                label='Inverkehrssetzungen',
                children=[
                    #html.H1(texts['page.title'], style={'textAlign': 'center'}),

                    # Header mit Titel + Schweizerwappen
                    html.Div([
                        html.Div(style={'width': '33%'}),  # Platz für Logo etc.
                        html.H1("Personenwagen-Dashboard", style={'margin': 0}),
                        html.Div(style={'width': '33%'}),  # Platz für Logo etc.
                    ], style={
                        'display': 'flex',
                        'justifyContent': 'space-between',
                        'alignItems': 'center',
                        'padding': '10px 20px'
                    }),

                    # 1st line: CH map and canton / municipality map
                    html.Div([
                        dcc.Graph(id='choropleth-map-ivs', style={
                            'width': '67%',
                            'border': '1px solid black',
                            'border-radius': '10px',
                            'overflow': 'hidden',
                            'margin-left': '10px'
                        }),
                        html.Div(id='right-panel-ivs', style={
                            'width': '33%',
                            'border': '1px solid black',
                            'border-radius': '10px',
                            'overflow': 'hidden',
                            'margin-right': '10px',
                            'background-color': 'white',
                            'padding': '10px'
                        })
                    ], style={
                        'display': 'flex',
                        'flexDirection': 'row',
                        'width': '100%',
                        'gap': '10px',
                        'justifyContent': 'center',
                        'alignItems': 'stretch',
                        'marginBottom': '20px',
                        'height': '450px'
                    }),

                    # 2nd line: Home-Button, year slider + toggle
                    html.Div([
                        html.Div(
                            html.Img(
                                id="home-button-ivs",
                                src="/assets/swisscoat.png",
                                title="Zur Ausgangsansicht zurückkehren",
                                n_clicks=0,
                                style={
                                    'height': '40px',
                                    'cursor': 'pointer',
                                    'marginRight': '20px',
                                }
                            ), style={'width': '10%', 'display': 'flex', 'justifyContent': 'center'},
                        ),
                        html.Div(
                            dcc.Slider(
                                id='year-slider-ivs',
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
                            style={'width': '60%'}
                        ),
                        html.Div(
                            daq.ToggleSwitch(
                                id='value-mode-toggle-ivs',
                                label='Relativ',
                                labelPosition='top',
                                value=True
                            ),
                            style={'width': '10%', 'textAlign': 'center', 'justifyContent': 'center', 'display': 'flex'}
                        ),
                    ], style={
                        'display': 'flex',
                        'flexDirection': 'row',
                        'alignItems': 'center',
                        'justifyContent': 'space-between',
                        'width': 'auto',
                        'margin': '10px',
                        'padding': '10px',
                        'background-color': 'white',
                        'border': '1px solid black',
                        'border-radius': '10px',
                        'overflow': 'hidden',
                        'gap': '10px',
                    }),

                    # additional graphs (3 side-by-side)
                    html.Div([
                        html.Div(dcc.Graph(id='stackedbar-fuel-stock-canton-ivs', style={'height': '100%'}),
                                 style={'width': '33%', 'border': '1px solid black',
                                        'boxSizing': 'border-box',
                                        'border-radius': '25px',
                                        'overflow': 'hidden'}),
                        html.Div(dcc.Graph(id='pie-fuel-stock-ivs', style={'height': '100%'}),
                                 style={'width': '33%', 'border': '1px solid black',
                                        'boxSizing': 'border-box',
                                        'border-radius': '25px',
                                        'overflow': 'hidden'}),
                        html.Div(id='summary-container-ivs', style={'width': '33%', 'border': '1px solid black',
                                                                'boxSizing': 'border-box',
                                                                'border-radius': '25px',
                                                                'overflow': 'hidden',
                                                                'backgroundColor': 'white',
                                                                'padding': '10px', })
                    ], style={
                        'display': 'flex',
                        'flexDirection': 'row',
                        'justifyContent': 'space-between',
                        'alignItems': 'stretch',
                        'width': '100%',
                        'gap': '10px',
                        'padding': '10px',
                        'height': '325px'
                    }),

                    # define stores (callback chaining)
                    html.Div([
                        dcc.Store(id="selected-canton-ivs", data="CH"),
                        dcc.Store(id="selected-municipality-ivs")
                    ], id="hidden-stores-ivs", style={"display": "none"})
                ],
                style={
                    'padding': '12px',
                    'fontSize': '18px',
                    'fontWeight': 'bold',
                    'backgroundColor': 'white',
                    'color': 'black',
                    'border': '2px solid black',
                    'border-top-left-radius': '50px'
                },
                selected_style={
                    'padding': '12px',
                    'fontSize': '18px',
                    'fontWeight': 'bold',
                    'backgroundColor': 'red',
                    'color': 'black',
                    'border': '2px solid black',
                    'borderBottom': 'none',
                    'border-top-left-radius': '50px'
                })
        ], style={'backgroundColor': 'white'})
    ], style={'backgroundColor': 'red'})
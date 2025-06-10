import dash.html as html
import dash.dcc as dcc
import dash_daq as daq
from click import style

from helper.general import available_years, default_year

# initialize logger
import logging
from helper.misc import log_current_function
logger = logging.getLogger(__name__)

texts = {'page.title':'Personenwagen-Dashboard',
         'title_colorbar':'Anzahl'}

def create_layout():
    log_current_function(level=logging.INFO, msg=f"{__name__}")
    return html.Div([
        html.Div([
            html.Div(style={'width': '5%'}), # Platz für Logo etc.
            html.H1("Personenwagen-Dashboard", style={'margin': 0, 'font-size':'2vw'}),
            html.Div(html.A(
                  html.Img(
                      src="/assets/info_icon.png",
                      style={'height': '5vh','cursor': 'pointer','padding': '5px'}),
                  href="/assets/readme.txt",  # Oder externer Link
                  target="_blank",
                  style={'textDecoration': 'none'}),style={'width': '5%'}),  # Platz für Logo etc.
            # Info-Button mit Bild
              ],
            style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'padding': '20px 2px',
            'backgroundColor':'white'}),
        dcc.Tabs([
            dcc.Tab(
                label='Bestand',
                children=[
                    # first line (navigation)
                    html.Div([
                        html.Div([
                            html.Img(
                                id="home-button",
                                src="/assets/swisscoat.png",
                                title="Zur Ausgangsansicht zurückkehren",
                                n_clicks=0,
                                style={
                                    'height': '40px',
                                    'cursor': 'pointer',
                                    'marginRight': '20px',
                                },
                            ), html.Span("zur Ausgangsansicht", style={'margin-right': '10px', 'fontSize': '1vw'}
                                         ), ],
                            style={'width': '20%', 'display': 'flex', 'justifyContent': 'left', 'paddingLeft': '20px'},

                        ),
                        html.Div(
                            dcc.Slider(
                                id='year-slider',
                                min=int(min(available_years)),
                                max=int(max(available_years)),
                                step=1,
                                value=int(default_year),
                                marks={int(year): str(year) for year in sorted(available_years)},
                                tooltip={"placement": "bottom", "always_visible": True},
                                className='custom-slider'
                            ),
                            style={'width': '60%'}
                        ),
                        html.Div(
                            children=[
                                html.Span("absolut", style={'margin-right': '10px', 'fontSize': '1vw'}),
                                daq.ToggleSwitch(
                                    id='value-mode-toggle',
                                    value=True,
                                    style={'display': 'inline-block'}
                                ),
                                html.Span("relativ",
                                          style={'margin-left': '10px', 'margin-right': '20px', 'fontSize': '1vw'}),
                            ],
                            style={'width': '20%', 'textAlign': 'center', 'justifyContent': 'center', 'display': 'flex',
                                   'alignItems': 'center'},
                        ),
                    ], style={
                        'display': 'flex',
                        'flexDirection': 'row',
                        'alignItems': 'center',
                        'justifyContent': 'space-between',
                        'width': 'auto',
                        'marginTop': '10px',
                        'marginLeft': '10px',
                        'marginRight': '10px',
                        'padding': '10px',
                        'background-color': 'white',
                        'border': '1px solid gray',
                        'border-radius': '10px',
                        'overflow': 'hidden',
                        'gap': '10px',
                    }),
                    # second line (map)
                    html.Div([
                        dcc.Graph(id='choropleth-map',
                                  config={"scrollZoom":False}, style={
                            'flex':'2',
                            'border': '1px solid gray',
                            'border-radius': '10px',
                            'overflow': 'hidden',
                            'height': '100%',
                            'minHeight': '40vh',
                        }),
                        html.Div(id='right-panel', style={
                            'flex':'1',
                            'border': '1px solid gray',
                            'border-radius': '10px',
                            'overflow': 'hidden',
                            'background-color':'white',
                            'padding': '5px',
                            'paddingLeft':'20px',
                            'height': '100%',
                            'minHeight': '40vh',

                        })
                    ], style={
                        'display': 'flex',
                        'flexDirection': 'row',
                        'width': '100%',
                        'gap': '10px',
                        'justifyContent': 'center',
                        'alignItems': 'stretch',
                        'marginTop': '10px',
                        'height': '40vh',
                        'paddingRight': '10px',
                        'paddingLeft': '10px',
                    }),


                    # 3rd line (additional graphs)
                    html.Div([
                        html.Div([
                        html.Div(dcc.Graph(id='stackedbar-fuel-stock-canton', style={'height': '100%'}), style={
                            'flex':'1',
                            'border': '1px solid gray',
                            'boxSizing': 'border-box',
                            'border-radius': '10px',
                            'overflow': 'hidden',
                            'height': '38vh',
                        }),
                        html.Div(dcc.Graph(id='pie-fuel-stock', style={'height': '100%'}), style={
                            'flex':'1',
                            'border': '1px solid gray',
                            'boxSizing': 'border-box',
                            'border-radius': '10px',
                            'overflow': 'hidden',
                            'height': '38vh',
                        }),
                            ],style={
                            'gap': '10px',
                            'flex':'2',
                            'flexDirection': 'row',
                            'display': 'flex',
                        }),
                        html.Div(id='summary-container', style={
                            'flex':'1',
                            'border': '1px solid gray',
                            'boxSizing': 'border-box',
                            'border-radius': '10px',
                            'overflow': 'hidden',
                            'backgroundColor': 'white',
                            'padding': '5px',
                            'paddingLeft':'20px',
                            'height': '38vh',
                        }),
                    ], style={
                        'display': 'flex',
                        'flexDirection': 'row',
                        'width': '100%',
                        'justifyContent': 'center',
                        'alignItems': 'stretch',
                        'marginTop': '10px',
                        'height': 'auto',
                        'paddingRight': '10px',
                        'paddingLeft': '10px',
                        'gap': '10px',
                    }),

                    # define stores (callback chaining)
                    html.Div([
                        dcc.Store(id="selected-canton", data="CH"),
                        dcc.Store(id="selected-municipality")
                    ], id="hidden-stores", style={"display": "none"})
                ],
                style={
                    'padding': '3px',
                    'fontSize': '1.3vw',
                    'fontWeight': 'bold',
                    'backgroundColor': 'white',
                    'color': 'black',
                    'border': '2px solid gray',
                    'border-top-right-radius': '50px',
                    'height':'3vw'
                },
                selected_style={
                    'padding': '3px',
                    'fontSize': '1.3vw',
                    'fontWeight': 'bold',
                    'backgroundColor': 'darkgray',
                    'color': 'black',
                    'border': '2px solid gray',
                    'borderBottom': 'none',
                    'border-top-right-radius': '50px',
                    'height': '3vw'
                }
            ),
            # second tab
            dcc.Tab(
                label='Inverkehrsetzungen',
                children=[
                    # first line (navigation)
                    html.Div([
                        html.Div([
                            html.Img(
                                id="home-button-ivs",
                                src="/assets/swisscoat.png",
                                title="Zur Ausgangsansicht zurückkehren",
                                n_clicks=0,
                                style={
                                    'height': '40px',
                                    'cursor': 'pointer',
                                    'marginRight': '20px',
                                },
                            ), html.Span("zur Ausgangsansicht",
                                         style={'margin-right': '10px', 'fontSize': '1vw'}
                                         ), ],
                            style={'width': '20%', 'display': 'flex', 'justifyContent': 'left', 'paddingLeft': '20px'},

                        ),
                        html.Div(
                            dcc.Slider(
                                id='year-slider-ivs',
                                min=int(min(available_years)),
                                max=int(max(available_years)),
                                step=1,
                                value=int(default_year),
                                marks={int(year): str(year) for year in sorted(available_years)},
                                tooltip={"placement": "bottom", "always_visible": True},
                                className='custom-slider'
                            ),
                            style={'width': '60%'}
                        ),
                        html.Div(
                            children=[
                                html.Span("absolut", style={'margin-right': '10px', 'fontSize': '1vw'}),
                                daq.ToggleSwitch(
                                    id='value-mode-toggle-ivs',
                                    value=True,
                                    style={'display': 'inline-block'}
                                ),
                                html.Span("relativ",
                                          style={'margin-left': '10px', 'margin-right': '20px', 'fontSize': '1vw'}),
                            ],
                            style={'width': '20%', 'textAlign': 'center', 'justifyContent': 'center', 'display': 'flex',
                                   'alignItems': 'center'},
                        ),
                    ], style={
                        'display': 'flex',
                        'flexDirection': 'row',
                        'alignItems': 'center',
                        'justifyContent': 'space-between',
                        'width': 'auto',
                        'marginTop': '10px',
                        'marginLeft': '10px',
                        'marginRight': '10px',
                        'padding': '10px',
                        'background-color': 'white',
                        'border': '1px solid gray',
                        'border-radius': '10px',
                        'overflow': 'hidden',
                        'gap': '10px',
                    }),
                    # second line (map)
                    html.Div([
                        dcc.Graph(id='choropleth-map-ivs',
                                  config={"scrollZoom":False}, style={
                            'flex':'2',
                            'border': '1px solid gray',
                            'border-radius': '10px',
                            'overflow': 'hidden',
                            'margin-left': '10px',
                            'height': '100%',
                            'minHeight': '40vh'
                        }),
                        html.Div(id='right-panel-ivs', style={
                            'flex':'1',
                            'border': '1px solid gray',
                            'border-radius': '10px',
                            'overflow': 'hidden',
                            'margin-right': '10px',
                            'background-color': 'white',
                            'padding': '5px',
                            'paddingLeft':'20px',
                            'height': '100%',
                            'minHeight': '40vh'
                    }),
                    ], style={
                        'display': 'flex',
                        'flexDirection': 'row',
                        'width': '100%',
                        'gap': '10px',
                        'justifyContent': 'center',
                        'alignItems': 'stretch',
                        'marginTop': '10px',
                        'height': '40vh',
                    }),



                    # 3rd line (additional graphs)
                    html.Div([
                        html.Div([
                        html.Div(dcc.Graph(id='stackedbar-fuel-stock-canton-ivs', style={'height': '100%'}), style={
                            'flex': '1',
                            'border': '1px solid gray',
                            'boxSizing': 'border-box',
                            'border-radius': '10px',
                            'overflow': 'hidden',
                            'height': '38vh',
                        }),
                        html.Div(dcc.Graph(id='pie-fuel-stock-ivs', style={'height': '100%'}), style={
                            'flex': '1',
                            'border': '1px solid gray',
                            'boxSizing': 'border-box',
                            'border-radius': '10px',
                            'overflow': 'hidden',
                            'height': '38vh',
                        }),
                    ], style={
                        'gap': '10px',
                        'flex': '2',
                        'flexDirection': 'row',
                        'display': 'flex',
                    }),
                        html.Div(id='summary-container-ivs', style={
                            'flex':'1',
                            'border': '1px solid gray',
                            'boxSizing': 'border-box',
                            'border-radius': '10px',
                            'overflow': 'hidden',
                            'backgroundColor': 'white',
                            'padding': '5px',
                            'paddingLeft':'20px',
                            'height': '38vh',
                        })
                    ], style={
                        'display': 'flex',
                        'flexDirection': 'row',
                        'width': '100%',
                        'justifyContent': 'center',
                        'alignItems': 'stretch',
                        'marginTop': '10px',
                        'height': 'auto',
                        'paddingRight': '10px',
                        'paddingLeft': '10px',
                        'gap': '10px',
                    }),

                    # define stores (callback chaining)
                    html.Div([
                        dcc.Store(id="selected-canton-ivs", data="CH"),
                        dcc.Store(id="selected-municipality-ivs")
                    ], id="hidden-stores-ivs", style={"display": "none"})
                ],
                style={
                    'padding': '3px',
                    'fontSize': '1.3vw',
                    'fontWeight': 'bold',
                    'backgroundColor': 'white',
                    'color': 'black',
                    'border': '2px solid gray',
                    'border-top-left-radius': '50px',
                    'height': '3vw'
                },
                selected_style={
                    'padding': '3px',
                    'fontSize': '1.3vw',
                    'fontWeight': 'bold',
                    'backgroundColor': 'darkgray',
                    'color': 'black',
                    'border': '2px solid gray',
                    'borderBottom': 'none',
                    'border-top-left-radius': '50px',
                    'height':'3vw'
                }
            )
        ], style={
            'fontWeight': 'bold',
            'border': 'none',
            'fontSize': '18px',
            'backgroundColor': 'white',
        })
    ], style={'height': '100vh', 'display': 'flex', 'flexDirection': 'column'})
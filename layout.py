import dash.html as html
import dash.dcc as dcc
import dash_daq as daq

from components.municipality_map import generate_map_municipality
from helper.general import available_years, default_year
from components.canton_map import generate_map_canton

# keep texts centralized
texts = {'page.title':'Personenwagen-Dashboard',
         'title_colorbar':'Anzahl'}

# functions
def create_layout():
    return html.Div([
        # Header mit Titel + Schweizerwappen
        html.Div([
            html.H1("Personenwagen-Dashboard", style={'margin': 0}),
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'padding': '10px 20px'
        }),
            
            # 1st line: CH map and canton / municipality map
            html.Div([
                dcc.Graph(id='choropleth-map', style={'width': '67%'}),
                html.Div(id='right-panel', style={'width': '33%'})
            ], style={
                'display': 'flex',
                'flexDirection': 'row',  # nebeneinander
                'width': '100%',
                'gap': '10px',
                'justifyContent': 'center',
                'alignItems': 'stretch',
                'marginBottom': '20px'
            }),

            # 2nd line: Home-Button, year slider + toggle
            html.Div([
                html.Img(
                    id="home-button",
                    src="/assets/swisscoat.png",
                    title="Zur Ausgangsansicht zurückkehren",
                    n_clicks=0,
                    style={
                        'height': '40px',
                        'cursor': 'pointer',
                        'marginRight': '20px'
                    }
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
                        value=False
                    ),
                    style={'width': '10%', 'textAlign': 'center', 'marginLeft': 'auto'}
                )
            ], style={
                'display': 'flex',
                'flexDirection': 'row',
                'alignItems': 'center',
                'justifyContent': 'space-between',
                'width': '80%',
                'margin': '20px auto'
            }),

            # additional graphs (3 side-by-side)
            html.Div([
                html.Div(dcc.Graph(id='stackedbar-fuel-stock-canton', style={'height': '100%'}), style={'width': '33%'}),
                html.Div(dcc.Graph(id='pie-fuel-stock', style={'height': '100%'}), style={'width': '33%'}),
                html.Div(id='summary-container', style={'width': '33%'})
            ], style={
                'display': 'flex',
                'flexDirection': 'row',
                'justifyContent': 'space-between',
                'alignItems': 'stretch',
                'width': '100%',
                'gap': '10px',
                'padding': '10px'
            }),

            # define stores (callback chaining)
            html.Div([
                dcc.Store(id="selected-canton", data="CH"),
                dcc.Store(id="selected-municipality")
            ], id="hidden-stores", style={"display": "none"})
        ])

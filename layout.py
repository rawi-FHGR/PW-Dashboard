import dash.html as html
import dash.dcc as dcc

from helper.general import available_years, default_year

# variables
texts = {'page.title':'Personenwagen-Dashboard',
         'title_colorbar':'Anzahl'}

# functions
def create_layout():
    return html.Div([
    html.H1(texts['page.title'], style={'textAlign': 'center'}),

    # Wrapper: zentriert die Inhalte in einer Spalte
    html.Div([
        # Choropleth Map
        html.Div(
            dcc.Graph(id='choropleth-map'),
            style={'width': '40%', 'textAlign': 'center'}
        ),

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
        )
    ],
    style={
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'center',
        'padding': '10px',
        'marginTop': '5px',
        'backgroundColor': '#f9f9f9'
    })
])

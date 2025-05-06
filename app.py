import dash
import dash_bootstrap_components as dbc

# project specific imports
import layout as layout
from callbacks import register_callbacks

# setup dash application
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])

# apply the layout to the app
app.layout = layout.create_layout()

# get the callback functions
register_callbacks(app)

# execute the app
if __name__ == '__main__':
    app.run(debug=True)

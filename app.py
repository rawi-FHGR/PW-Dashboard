import dash
import dash_bootstrap_components as dbc
import logs.logging_config

# project specific imports
import layout as layout
from callbacks import register_callbacks

# setup dash application
app = dash.Dash(__name__,
                external_stylesheets = [dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True)      # due to dynamic component generation

# apply the layout to the app
app.layout = layout.create_layout()

# get the callback functions
register_callbacks(app)

# execute the app
if __name__ == '__main__':
    # setup debug to False in production environment
    app.run(debug=True)

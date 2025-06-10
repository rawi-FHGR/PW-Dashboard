import dash
import dash_bootstrap_components as dbc
import logs.logging_config

# project specific imports
import layout as layout
from callbacks import register_callbacks

# setup dash application
app = dash.Dash(__name__, title="Personenwagen CH",
                external_stylesheets = [dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True)      # due to dynamic component generation

# apply the layout to the app
app.layout = layout.create_layout()

# get the callback functions
register_callbacks(app)

# execute the app
if __name__ == '__main__':
    # setup debug to False in production environment
    # development mode (local)
    #app.run(debug=True, host='127.0.0.1', port=8050)

    # production mode
    app.run(debug=False, host='0.0.0.0', port=8080)

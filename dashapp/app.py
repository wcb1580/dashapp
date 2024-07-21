import dash
import dash_bootstrap_components as dbc
from flask_caching import Cache
from layout import layout  # Import the layout
from callbacks import register_callbacks  # Import the callback registration function

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# Configure Caching
cache = Cache(app.server, config={'CACHE_TYPE': 'simple'})

# Set the layout of the app
app.layout = layout

# Register callbacks
register_callbacks(app, cache)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

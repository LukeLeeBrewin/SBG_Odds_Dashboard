from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from flask import Flask
import plotly.express as px
import pandas as pd
import numpy as np

from fightstab import *

external_stylesheets = [dbc.themes.DARKLY]
server = Flask(__name__)
app = Dash(__name__, suppress_callback_exceptions=True,external_stylesheets=external_stylesheets, server=server,prevent_initial_callbacks=True)





# Define Sub Tabs
tab_objects = [FightTab()]


# Register all calllbacks
dash_tabs = []
for tab in tab_objects:
    tab.register_callbacks(app)
    dash_tabs.append( dbc.Tab(tab.build_tab(), label=tab.LABEL, tab_id=tab.ID) )

app.layout = html.Div(children=[
            dbc.Tabs(
                    id="tabs",
                    children=dash_tabs
                    )
            ],
            )

# Run app
if __name__=='__main__':
    app.run_server(debug=True)

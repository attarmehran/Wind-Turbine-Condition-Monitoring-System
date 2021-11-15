from app import app
import dash_bootstrap_components as dbc
import page1FarmView as F
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import page1FarmView
from farmView.callbacksPage1FarmView import *
from turbineView.callbacksPage1TurbineView import *
from dbManager.callbacksDbManager import *
import callbacksTrendmonitoring

app.layout = dbc.Container([
    F.generate_navbar(app),
    html.Br(),
    F.content,
    html.Br(),
], fluid=True)

app.title = "WTCM Platform"

if __name__ == '__main__':
    #app.run_server(host='0.0.0.0',debug=False,port=8080,dev_tools_ui=False,dev_tools_props_check=False)#MapnaMind
    app.run_server(debug=True,port=8000,dev_tools_ui=True,dev_tools_props_check=True)#ShayanLaptop


import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import pandas as pd
import turbineView.Analysis_Tools as AT
from page1TurbineView import  *


CONTENT_STYLE = {
    "margin-left": "0rem",
    # "margin-right": "1rem",
    # "padding": "1rem 1rem",
    "border-style": "solid",
}

def generate_select_farm_drpdwn():
    farm_drpdwn_dbc = dbc.FormGroup(
        [
            dbc.Label("Select  Wind Farm  "),
            dbc.Select(
                id="select-farm",
                options=[
                    {'label': 'Kahak', 'value': 'Kahak'},
                    {'label': 'Aqkand', 'value': 'Aqkand', "disabled": True},
                    {'label': 'Fars', 'value': 'Fars', "disabled": True}
                ],
                value="Kahak",
                style={'width': "25%", 'margin-left': "5px"}

            ),
        ],
        inline=True
    )
    return farm_drpdwn_dbc

def generate_check_list():
    checklist = dcc.Checklist(
        id='checklist-WT-selection',
        # className = 'my_box_container',
        inputClassName='my_box_input',
        labelClassName='my_box_label',
    )
    return checklist


def generate_navbar(app):
    MAPNAlogo = dbc.Row(
        [
            dbc.Col(
                html.Img(src=app.get_asset_url("MAPNAlogo.png"), height="80px"),
                md=4,
            ),
        ],
        no_gutters=True,
        className="ml-auto flex-nowrap mt-3 mt-md-0",
        align="center",
        justify="start",
    )

    navbar = dbc.Navbar(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=app.get_asset_url("WINDCARE_LOGO (1).png"), height="80px"), md=2),
                        dbc.Col(dbc.NavbarBrand("MAPNA Wind Turbine Condition Monitoring Platform", className="ml-2"), md=6),
                    ],
                    align="center",
                    no_gutters=True,
                    justify="start",

                ),
            ),
            MAPNAlogo,
        ],
        color="dark",
        dark=True,
    )
    return navbar


def generate_card_deck():
    cards = html.Div([
        dbc.Row([
            dbc.Col(dbc.Card(
                [
                    dbc.CardBody(
                        [
                            dbc.Row([
                                dbc.Col(dbc.CardImg(src="/assets/WindTurbine2.png", bottom=True), width=3),
                                dbc.Col([html.H4(id='farm-speed-card', className="card-title"), html.H6("wind Speed, m/s")])

                            ]),
                        ],style={'padding':'0.25rem'}
                    )
                ],
                color="danger",
            )),
            dbc.Col(dbc.Card(
                [
                    dbc.CardBody(
                        [
                            dbc.Row([
                                dbc.Col(dbc.CardImg(src="/assets/electricity.png", bottom=True), width=3),
                                dbc.Col([html.H4(id='farm-generation-card', className="card-title"), html.H6("Total Generation, kW")])

                            ]),
                        ],style={'padding':'0.25rem'}
                    )
                ],
                color="danger",
            )),
            dbc.Col(dbc.Card(
                [
                    dbc.CardBody(
                        [
                            dbc.Row([
                                dbc.Col(dbc.CardImg(src="/assets/frequency.jpg", bottom=True), width=3),
                                dbc.Col([html.H4(id='farm-freq-card', className="card-title"), html.H6("Frequency, Hz")])
                            ]),
                        ],style={'padding':'0.25rem'}
                    )
                ],
                color="danger",
                inverse=True,

            )),
            dbc.Col(dbc.Card(
                [
                    dbc.CardBody(
                        [
                            dbc.Row([
                                dbc.Col(dbc.CardImg(src="/assets/temp_icon.png", bottom=True, ), width=3),
                                dbc.Col([html.H4(id='farm-temperature-card',className="card-title"), html.H6("Ambient Temperature, °C")])
                            ]),
                        ],style={'padding':'0.25rem'}
                    )
                ],
                color="danger",

            ))
        ])
    ])
    return cards


def generate_liveData_farm():
    AT.generate_hdf_live_data()
    livedata = [html.Br(), generate_select_farm_drpdwn(), html.Br(), generate_check_list(), html.Br(), html.Div(id='table-container-live-data'),
                html.Br(), generate_card_deck()]
    return livedata


farm_view_tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Live Data", tab_id="tab-live-data"),
                # dbc.Tab(label="Favorites", tab_id="tab-favorites"),
                # dbc.Tab(label="Tab3", tab_id="tab-3-internal"),
            ],
            id="farm-view-tabs",
            active_tab="tab-live-data",
        ),
        html.Div(id="tabs-farm-view-div", style={'padding': '1rem' '1rem'}),
    ]
)

card = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Farm View", tab_id="farm-view"),
                    dbc.Tab(label="Turbine View", tab_id="turbine-view"),
                    dbc.Tab(label="DB Manager", tab_id="db-manager"),
                    dbc.Tab(label="Trend Monitoring", tab_id="trend-monitoring")
                ],
                id="overview-card-tabs",
                card=True,
                active_tab="farm-view",
                # style = {}
            )
        ),
        html.Br(),
        dbc.CardBody(html.Div(id="farm-view", style={'padding': '1rem' '1rem'})),
    ]
)

content = html.Div(id="page1-content", children=card, style=CONTENT_STYLE)

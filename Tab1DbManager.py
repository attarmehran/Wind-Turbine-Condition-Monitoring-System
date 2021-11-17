import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

CONTENT_STYLE = {
    "margin-left": "0rem",
    "margin-right": "0rem",
    # "padding": "1rem 1rem",
    # "border-style": "solid",
}


def generate_main_tabs():
    tabs = dbc.Card(
        [
            dbc.CardHeader(
                dbc.Tabs(
                    [
                        dbc.Tab(label="Main", tab_id="main-tab1"),
                        dbc.Tab(label="Classifier", tab_id="classifier-tab"),
                    ],
                    id="dbManager-tabs",
                    card=True,
                    active_tab="main-tab1",
                    className="tabs__container",
                )
            ),
            html.Br(),
            dbc.CardBody(html.Div(id="dbManager-main-content")),
        ]
    )
    return tabs


# dbManager_content = html.Div(id="dgManager_page", children=[ generate_main_tabs()
#
# ], style=CONTENT_STYLE)


def generate_select_farm_drpdwn():
    farm_drpdwn_dbc = dbc.FormGroup(
        [
            # dbc.Label("Select  Wind Farm"),
            dbc.Select(
                id="select-farm",
                options=[
                    {'label': 'Kahak', 'value': 'Kahak'},
                    {'label': 'Aqkand', 'value': 'Aqkand', "disabled": True},
                    {'label': 'Fars', 'value': 'Fars', "disabled": True}
                ],
                value="Kahak",
                style={'width': "100%", 'margin-left': "0px"}

            ),
            # dbc.FormText("Choose a Time",id='selected-farm',style={'width':"25%",'margin-left':"5px"}),

        ],
        inline=True
    )
    return farm_drpdwn_dbc

def generate_check_list():
    t = 22
    turbine_number = [i for i in range(1, t + 1)]
    turbines = ["%02d" % n for n in turbine_number]

    checklist = dcc.RadioItems(
        id='radioItem-WT-selection',
        options=[{'label': "WTG {}".format(i), 'value': "{}".format(i)} for i in turbines],
        value="01",
        inputClassName='my_box_input',
        labelClassName='icon-windturbine',
        labelStyle={'display': 'inline-block', 'width': '7em'}
    )
    return checklist


def card(name):
    card = dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.Row([
                        dbc.Col(dbc.CardImg(src="/assets/WINDCARE_LOGO.png", style={'width': '35px'}, bottom=True),
                                width=4),
                        dbc.Col([html.H6(children=name, className="card-title",style={'margin-right':'0px','padding':'0px','color':'red'}),
                                 html.Div(id=name, style={'font-size': "10px",'margin':'0px'})], width=8)

                    ]),
                ]
            )
        ],
        style={"width": "100%", 'margin-top': '2px'},
        color="danger",
        outline=True

    )
    return card


text_area = dbc.FormGroup(
    [
        dbc.Label("Database Status"),
        dcc.Loading(html.Div(id='textarea-example',
                             style={'width': '100%', 'height': 150, 'Y-overflow': 'True', 'borderStyle': 'solid',
                                    'borderRadius': '5px', 'background-color': 'gray'}))
    ])
upload_button = dcc.Upload(
    id='upload-data',
    children=html.Div([
        'Drag and Drop or ',
        html.A('Select Files')
    ]),
    style={
        'width': '100%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '0px',
        'justify': 'center'
    },
    # Allow multiple files to be uploaded
    multiple=True
)

update = dbc.FormGroup(
    [
        dbc.Label("Update Main Database"),
        dbc.Button("Update", id='Update-button', color="Success", style={'margin-left': '5px'})])

second_column = dbc.Row([dbc.Col([card('WTG 01'), card('WTG 02'), card('WTG 03'), card('WTG 04'), card('WTG 05')]),
                         dbc.Col([card('WTG 06'), card('WTG 07'), card('WTG 08'), card('WTG 09'), card('WTG 10')]),
                         dbc.Col([card('WTG 11'), card('WTG 12'), card('WTG 13'), card('WTG 14'), card('WTG 15')]),
                         dbc.Col([card('WTG 16'), card('WTG 17'), card('WTG 18'), card('WTG 19'), card('WTG 20')]),
                         dbc.Col([card('WTG 21'), card('WTG 22')])
                         ])

style = {'border': 'solid', 'padding-top': '10px', 'align': 'center', 'justify': 'center', 'padding-left': '1px',
         'padding-right': '1px', 'margin': "2px"}
content = dbc.Row([
    dbc.Col([generate_select_farm_drpdwn(), generate_check_list()], md=2, align='center', style=style),
    dbc.Col(second_column, md=7,
            style={'border': 'solid', 'padding': '5px', 'margin': "0.1px", 'display': 'inline-block'}),
    dbc.Col([text_area, upload_button, html.Div(html.Img(src='/assets/Picture1.png', width='100%'))], md=2,
            style=style),
], justify='around')

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import Tab1DbManager as Tab1


center_sytle= {'width': '100%', 'display': "flex", "align-items": "center", "justify-content": "center",'font-family':'Comic Sans'}


select_year = dbc.Form(
    [
        dbc.FormGroup(
            [
                dbc.Label("Year", className="mr-2",style={'display': "flex", "align-items": "center", "justify-content": "center",'margin-top':'20px'}),
                dbc.Input(type="Number", id='Year',placeholder="Select year",value=2020,min=2019, max=2021, step=1),
            ],
            className="mr-3",
            style={'width':'100%'}
        ),])

inline_radioitems = dbc.FormGroup(
    [
        dbc.Label("Select Season",style={'display': "flex", "align-items": "center", "justify-content": "center",'margin-top':'20px'}),
        dbc.RadioItems(
            options=[
                {"label": "Spring", "value": 'spring'},
                {"label": "Summer", "value": 'summer'},
                {"label": "Autumn", "value": 'autumn'},
                {"label": "Winter", "value": 'winter'},

            ],
            value='spring',
            id="radioitems-season",
            inline=True,
            style={'justify-content':'center'}
        ),
    ]
)

text_area_tab2 = dbc.FormGroup(
    [
        dbc.Label("Database Status"),
        dcc.Loading(html.Div(id='textarea-example-tab2',style={'width': '100%', 'height': 150, 'Y-overflow': 'True','borderStyle': 'solid',
        'borderRadius': '5px','background-color':'gray'}))
        ])

stratified_files = dbc.FormGroup(
    [
        # dbc.Label("Export Files"),
        dbc.Button("Export", id='export-button', color="Success",style={'margin-left': '5px','color':'black','background-color': 'lightsteelblue'})])


# style = {'border': 'solid', 'padding-top': '10px','align':'center', 'justify': 'center', 'margin': "0px","align-items": "center", "justify-content": "center"}

content = dbc.Row([dbc.Col([Tab1.generate_select_farm_drpdwn(),Tab1.generate_check_list()],md=2,style=Tab1.style),
                   dbc.Col([html.Div("Time Selection",style = center_sytle),html.Div(select_year,style=center_sytle),
                               html.Div(inline_radioitems,style=center_sytle),
                            html.Img(src='/assets/4-season-installation.png',width='100%')],style=Tab1.style,md=4),
                   dbc.Col([text_area_tab2,stratified_files],md=2,style=Tab1.style)
],justify='around')

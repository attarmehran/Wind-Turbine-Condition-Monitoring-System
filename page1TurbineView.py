import plotly.graph_objects as go
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import turbineView.Analysis_Tools as AT

card_background_color = '#7F797C'
img_border_style = {'display': 'flex', 'justify-content': 'center', "border-style": "solid",
                          'border-color': '#ff4d4d', 'border-width': '1px', 'border-radius': "0.25rem"
                          }
figure_border_style = {"border-style": "solid",
                          'border-color': '#ff4d4d', 'border-width': '1px', 'border-radius': "0.25rem"
                          }



def gen_turbine_view_select_turbine():
    list_of_turbines = [item for item in range(1, 23)]
    list_of_turbines = ["%02d" % n for n in list_of_turbines]

    div = dbc.FormGroup(
        [
            dbc.Label(html.Div('🔴')),
            # dbc.Label(html.H4("Kahak ➡ "), id='farm-label-turbine-view'),
            dbc.Label(html.H4("Kahak  "), id='farm-label-turbine-view'),
            dbc.Select(
                id="select-turbine",
                options=[
                    {'label': "WTG {}".format(i), 'value': "{}".format(i)} for i in list_of_turbines
                ],
                value=list_of_turbines[1],
                style={'width': "45%", 'margin-left': '5px'}

            ),
        ],
        inline=True
    )
    return div




def generate_technical_specifications():
    header_font_style = {'color': 'white'}
    body_font_style = {'color': 'white', 'fontSize': '14px', 'display': 'flex', 'justify-content': 'center'}
    Technical_Specification_card = dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.Row([
                        dbc.Col(dbc.CardImg(src="/assets/technical_spec.png", bottom=True), width=3),
                        dbc.Col([html.H5("Technical Specification", style=header_font_style)], align='center')

                    ], justify='end'),
                    html.Hr(),
                    dbc.Row([dbc.Col(html.Div("Last Update", style=body_font_style)),
                             dbc.Col(dbc.Spinner(html.Div(id='last_update_id', style=body_font_style), size="sm"))],
                            justify='between'),
                    html.Br(),
                    dbc.Row([dbc.Col(html.Div("Turbine Type", style=body_font_style)),
                             dbc.Col(dbc.Spinner(html.Div(id='turbine_type', style=body_font_style), size="sm"))],
                            justify='between'),
                    html.Br(),

                    dbc.Row([dbc.Col(html.Div("Rated Power, kW", style=body_font_style)),
                             dbc.Col(dbc.Spinner(html.Div(id='rated_power', style=body_font_style), size="sm"))],
                            justify='between'),
                    html.Br(),
                    dbc.Row([dbc.Col(html.Div("Power Setpoint", style=body_font_style)),
                             dbc.Col(dbc.Spinner(html.Div(id='power_setpoint', style=body_font_style), size="sm"))],
                            justify='between'),
                ], style={'padding': "3px"}
            )
        ],
        color="danger",
        outline=True

    )
    return Technical_Specification_card


second_row_height = 210

wind_speed_card = dbc.Card(
    [
        dbc.CardImg(src="/assets/143-512.png",
                    style={'height': "7rem", 'width': '7rem', 'display': 'flex', 'justify-content': 'center'},
                    top=True),

        dbc.CardBody(
            [
                dbc.Spinner(html.Div(id='wind-speed-card', className="card-title",
                                     style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                            'fontSize': 25,'color': 'white',})),
                html.P("m/s", style={'display': 'flex', 'justify-content': 'center', 'color': 'white', 'fontSize': 14}),
            ]
        ),
    ],
    style={'background': 'rgba(0,0,0,0)', 'height': second_row_height},
)


def gen_wind_direction_plot():
    fig = go.Figure()

    fig.add_trace(go.Barpolar(
        r=[77.5],
        name='11-14 m/s',
        marker_color='#ff4d4d'
    ))

    # fig.update_traces(text=['North', 'N-E', 'East', 'S-E', 'South', 'S-W', 'West', 'N-W'])
    fig.update_layout(
        # title='Wind Speed Distribution in Laurel, NE',
        font_size=10,
        legend_font_size=8,
        plot_bgcolor=card_background_color,
        polar_angularaxis_rotation=90,
        margin=dict(l=1, r=1, t=5, b=5),
        paper_bgcolor=card_background_color,
    )

    return fig





def gen_gap_card():
    main_style = {'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'padding-top': '2%', 'color': 'white',
                  'fontSize': 13,'background':card_background_color}
    degree_style = {'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'padding-top': '1%',
                    'color': 'white', 'fontSize': 25}
    content = dbc.Card(
        [

            dbc.CardBody(
                [html.Div('Wind Direction', style=main_style),
                 html.Div(id='wind_direction-stats', style=degree_style),
                 html.Div('Turbine Direction', style=main_style),
                 html.Div(id='turbine-direction-stats', style=degree_style),
                 html.Div('Gap', id='test', style=main_style),
                 html.Div(id='gap-direction', style=degree_style)]
            ),
        ],
        style={'background': 'rgba(0,0,0,0)','height': second_row_height,},
    )

    return content


uptime_style = {'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'padding-top': '1%',
                'color': '#ff4d4d', 'fontSize': '15px'}
body_font_style = {'color': 'white', 'fontSize': '14px', 'display': 'flex', 'justify-content': 'center'}
header_font_style = {'color': 'white'}

Productivity_card = dbc.Card(
    [
        dbc.CardBody(
            [
                dbc.Row([
                    dbc.Col(dbc.CardImg(src="/assets/newProductivity.png", bottom=True), width=3),
                    dbc.Col([html.H5("Productivity", style=header_font_style)], align='center')

                ], justify='end'),
                # html.Hr(),
                dbc.Row([

                    dbc.Col([html.H5("Uptime", style=uptime_style),
                             html.H6(id='uptime', style=body_font_style)], )

                ], justify='center'),
                # html.Hr(),
                dbc.Row([
                    dbc.Col([html.H5("Produced Energy, kWh", style=uptime_style)], )
                ], justify='center'),

                dbc.Row([dbc.Col(html.Div("Today", style=body_font_style)),
                         dbc.Col(dbc.Spinner(html.Div(id='today_production', style=body_font_style), size="sm"))],
                        justify='between'),
                dbc.Row([dbc.Col(html.Div("This Month", style=body_font_style)),
                         dbc.Col(dbc.Spinner(html.Div(id="month_production", style=body_font_style), size="sm"))],
                        justify='between'),
                dbc.Row([dbc.Col(html.Div("Total", style=body_font_style)),
                         dbc.Col(dbc.Spinner(html.Div(id='total-production', style=body_font_style), size="sm"))], justify='between'),
                dbc.Row([
                    dbc.Col([html.H5("Availability, %", style=uptime_style)], )
                ], justify='center'),
                dbc.Row([dbc.Col(html.Div("Avail. today", style=body_font_style)),
                         dbc.Col(dbc.Spinner(html.Div(id='today_avail', style=body_font_style), size="sm"))],
                        justify='between'),
                dbc.Row([dbc.Col(html.Div("Avail. this month", style=body_font_style)),
                         dbc.Col(dbc.Spinner(html.Div(id='month_avail', style=body_font_style), size="sm"))],
                        justify='between'),
                dbc.Row([dbc.Col(html.Div("Avail. total", style=body_font_style)),
                         dbc.Col(dbc.Spinner(html.Div(id='total_avail', style=body_font_style), size="sm"))],
                        justify='between')

            ], style={'padding': "3px"}
        )
    ],
    color="danger",
    outline=True

)



second_row_border_style = {'height': second_row_height,"border-style": "solid",
                          'border-color': '#ff4d4d', 'border-width': '1px', 'border-radius': "0.25rem",'padding':'0px','margin':'0px'
                          }

second_row = dbc.Row([
    dbc.Col(
        dbc.Spinner(html.Div(dcc.Graph(id='gauge-gen-speed',
                                       style=second_row_border_style))), md=2),
    dbc.Col(
        dbc.Spinner(html.Div(dcc.Graph(id='gauge-gen-power',
                                       style=second_row_border_style))), md=2),
    dbc.Col(dbc.Spinner(html.Div(wind_speed_card,style=second_row_border_style)), md=2, ),

    dbc.Col(dbc.Spinner(html.Div(gen_gap_card(),style=second_row_border_style)),  md=2),
    dbc.Col(dbc.Spinner(html.Div(dcc.Graph(id='bar-temp-comparison',
                                           style=second_row_border_style))), md=3),

],justify="center")



third_row = html.Div([
    dbc.Row([
    dbc.Col(dbc.Spinner(html.Div([dcc.Graph(id='power-curve-graph'), AT.gen_time_period_drpdown('power-curve-drpdwn')],style=figure_border_style)),
            md=6),
    dbc.Col(dbc.Spinner(html.Div(
        [dcc.Graph(id='production-statistics-graph'), AT.gen_time_period_drpdown('production-statistics-drpdwn')],style=figure_border_style)), md=6)
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col(dbc.Spinner(html.Div([dcc.Graph(id='rose-wind'),AT.gen_time_period_drpdown('windrose-drpdwn')],style=figure_border_style)),md=6),
        dbc.Col(dbc.Spinner(html.Div([dcc.Graph(id='working-class-graph'),AT.gen_time_period_drpdown("working-class-drpdwn")],style=figure_border_style)),md=6)
    ]),

])



turbine_view_content = html.Div([
    html.Div(id='Hidden-Div', style={'display': 'none'}),
    html.Div(id='Hidden-Div-production-statistics', style={'display': 'none'}),
    html.Div(id='Hidden-Div-windrose', style={'display': 'none'}),
    html.Div(id='Hidden-Div-working-class', style={'display': 'none'}),

    dbc.Row([
        dbc.Col([gen_turbine_view_select_turbine(), generate_technical_specifications()], md=4),
        dbc.Col(Productivity_card, md=4),
        dbc.Col([html.Div(html.Img(src='/assets/WindTurbineMapna.png', height=305), style=img_border_style)],
                md=4),
    ], justify='between',align="end"),
    html.Hr(),
    second_row,
    html.Hr(),
    third_row

])

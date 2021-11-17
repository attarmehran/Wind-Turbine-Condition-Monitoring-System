import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import Tab1DbManager as Tab1
import pandas as pd

center_sytle = {'width': '100%', 'display': "flex", "align-items": "center", "justify-content": "center",
                'font-family': 'Comic Sans'}


def generate_check_list():
    t = 22
    turbine_number = [i for i in range(1, t + 1)]
    turbines = ["%02d" % n for n in turbine_number]

    checklist = dcc.Checklist(
        id='checklist-unit-selection',
        options=[{'label': "WTG {}".format(i), 'value': "WTG {}".format(i)} for i in turbines],
        value=["WTG 01"],
        inputClassName='my_box_input',
        labelClassName='icon-windturbine',
        labelStyle={'display': 'inline-block', 'width': '7em'}
    )
    return checklist


select_start_date_time = dbc.FormGroup(
    [
        # dbc.FormText(id='date-information'),
        dbc.Label("Start", width=3),
        dbc.Col(dbc.Input(id='date-start-input', type="datetime-local", value='2020-01-01T04:40', size='1px'), width=9),
        dbc.FormText("Choose Start Time", id='date-start-result'),
    ], row=True
)
select_end_date_time = dbc.FormGroup(
    [
        dbc.Label("End", width=3),
        dbc.Col(dbc.Input(id='date-end-input', type="datetime-local", value='2020-10-04T23:40', size='1px'), width=9),
        dbc.FormText(children="Choose End Time", id='date-end-result'),
    ], row=True
)

class_list = [1, 2, 3, 4]
class_drpdwn = dbc.FormGroup(
    [
        dbc.Label("Class Mode Selection"),
        dbc.Col([
            dbc.Select(
                id="select-class-mode-drpdwn",
                options=[{'label': "Class {}".format(i), 'value': "{}".format(i)} for i in class_list],
                value=1,
                # style={'width': "100%",},
                bs_size='sm'
            ), ], md=12)
    ],
    row=True,

)

power = dbc.FormGroup(
    [dbc.Label("power (kW)"),
     dbc.Col(
         dbc.InputGroup(
             [
                 dbc.InputGroupAddon("Min", addon_type="prepend"),
                 dbc.Input(type="number", id="power_min"),
                 dbc.InputGroupAddon("Max", addon_type="prepend"),
                 dbc.Input(type="number", id="power_max"),
             ],
             # className="mb-3",
             size='sm'
         ), md=12)
     ], row=True
)
Nacelle_temp = dbc.FormGroup(
    [
        dbc.Label("Nacelle Temp (°C)"),
        dbc.Col(
            dbc.InputGroup(
                [
                    dbc.InputGroupAddon("Min", addon_type="prepend"),
                    dbc.Input(type="number", id="Nacelle_t_min"),
                    dbc.InputGroupAddon("Max", addon_type="prepend", ),
                    dbc.Input(type="number", id="Nacelle_t_max"),
                ],
                # className="mb-3",
                size='sm'
            ), md=12),
    ], row=True
)
pitch_angle = dbc.FormGroup([
    dbc.Label("Pitch angle (deg)"),
    dbc.Col(
        dbc.InputGroup(
            [
                dbc.InputGroupAddon("Min", addon_type="prepend"),
                dbc.Input(type="number", id="pitch_min"),
                dbc.InputGroupAddon("Max", addon_type="prepend"),
                dbc.Input(type="number", id="pitch_max"),
            ],
            # className="mb-3",
            size='sm'
        ), md=12),
], row=True)
gend_speed = dbc.FormGroup(
    [
        dbc.Label("Gens speed (Hz)"),
        dbc.Col(
            dbc.InputGroup(
                [
                    dbc.InputGroupAddon("Min", addon_type="prepend"),
                    dbc.Input(type="number", id="genspeed_min"),
                    dbc.InputGroupAddon("Max", addon_type="prepend"),
                    dbc.Input(type="number", id="genspeed_max"),
                ],
                # className="mb-3",
                size='sm'
            ), md=12),

    ], row=True,
)

data_type = dbc.FormGroup(
    [
        dbc.Label("Data Type"),
        dbc.Col([
            dbc.RadioItems(
                options=[
                    {"label": "Raw Data", "value": 'raw'},
                    {"label": "Processed Data", "value": 'processed'},
                ],
                value='raw',
                id="radioitems-data-type",
                inline=True,
            ),
        ], md=12)]
)
component_list = ['PLU 1', 'PLU 2', 'PLU 3', 'Gearbox', 'Main Bearing', 'Power Reduction', 'LVU', 'Miscellaneous',
                  'Wind Farm Management', 'Generator', 'Grid', 'Ambient', 'Converter', 'Rotor', 'Yaw']
component_selection = dbc.FormGroup(
    [
        dbc.Label("Component Selection",style={'fontSize': 25}),
        dbc.Col([
            dbc.RadioItems(
                options=[
                    {"label": "{}".format(i), "value": "{}".format(i)} for i in component_list],
                value=component_list[0],
                id="component-list-radio",
                labelClassName='trend_label',
                inline=False,

            ),
        ], md=12)]
)

sensor_selection = dbc.FormGroup(
    [
        dbc.Label("List of sensors",style={'fontSize': 25}),
        dbc.Col([
            dcc.Checklist(
                id='checklist-sensor-selection',
                # className = 'my_box_container',
                # inputClassName='my_box_input',
                labelStyle={'display': 'block'},
                labelClassName='trend_label',
            ),
        ], md=12)]
)

PLU_1 = ['PLU1 DC Current (A)', 'PLU1 PBU Temp (°C)', 'PLU1 PCH Temp (°C)', 'PLU1 PPS Temp (°C)',
         'PLU1 PCO HeatSink Temp (°C)', 'PLU1 PDU Temp (°C)',
         'PLU1 Pitch Angle PS1 (°)', 'PLU1 Voltage 1 (V)', 'PLU1 Voltage 2 (V)', 'PLU1 Voltage 3 (V)',
         'PLU1 Voltage 4 (V)']
PLU_2 = ['PLU2 DC Current (A)', 'PLU2 PBU Temp (°C)', 'PLU2 PCH Temp (°C)', 'PLU2 PPS Temp (°C)',
         'PLU2 PCO HeatSink Temp (°C)', 'PLU2 PDU Temp (°C)',
         'PLU2 Pitch Angle PS1 (°)', 'PLU2 Voltage 1 (V)', 'PLU2 Voltage 2 (V)', 'PLU2 Voltage 3 (V)',
         'PLU2 Voltage 4 (V)']
PLU_3 = ['PLU3 DC Current (A)', 'PLU3 PBU Temp (°C)', 'PLU3 PCH Temp (°C)', 'PLU3 PPS Temp (°C)',
         'PLU3 PCO HeatSink Temp (°C)', 'PLU3 PDU Temp (°C)',
         'PLU3 Pitch Angle PS1 (°)', 'PLU3 Voltage 1 (V)', 'PLU3 Voltage 2 (V)', 'PLU3 Voltage 3 (V)',
         'PLU3 Voltage 4 (V)']
Gearbox = ['MGB Oil Pressure (bar)', 'MGB Temp CoolWaterFlow (°C)', 'MGB Temp CoolWaterReturn (°C)',
           'MGB Temp Oil Sump (°C)',
           'MGB TempBearing 150 (°C)', 'MGB TempBearing 151 (°C)', 'MGB TempBearing 152 (°C)',
           'MGB TempBearing 450 (°C)',
           'MGB TempBearing 451 (°C)', 'MGB TempBearing 452 (°C)', 'MGB Delta Temp Cooling (°C)']
MainBearing = ['MB Oil Pressure IN (bar)', 'MB Oil Pressure Pp (bar)', 'MB Temp 1 (°C)', 'MB Temp 2 (°C)']
Power_Reduction = ['Power Reduction Cause', 'Red. Power setp. (kW)']
LVU = ['LVU Residual Current Guard (mA)', 'LVU Temp (°C)']
Miscellaneous = ['Temp Nacelle (°C)', 'Transfo Temp L1 (°C)', 'Tower Inside Temp (°C)', 'Wp4000_Idle_Time',
                 'Wp4000_Temp (°C)', '1.3.NQFlicker',
                 '1.3.PIAvg_32 (A)', '1.3.PPSum (kW)', '1.3.PQSum (kVAr)', '1.3.PVNet (V)', 'TB Temp (°C)']
Wind_Farm_Management = ['Active Power Set Point WFM (kW)', 'Active Power Set Point WFM internal (kW)']
Generator = ['Gen Temp Coil L1 (°C)', 'Gen Temp Coil L2 (°C)', 'Gen Temp Coil L3 (°C)', 'Gen Temp CoolWaterFlow (°C)',
             'Gen Temp CoolWaterReturn (°C)', 'GenTemp Bearing DE (°C)', 'GenTemp Bearing NDE (°C)',
             'Speed Generator (rpm)', 'Gen Delta Temp Coil L12 (°C)', 'Gen Delta Temp Coil L23 (°C)',
             'Gen Delta Temp Coil L13 (°C)', 'Gen Delta Temp Cooling Water (°C)']

Grid = ['GridCosPhi', 'GridCurrent (A)', 'GridFrequency (Hz)', 'GridReactivePower (kVAr)', 'GridRealPower (kW)',
        'GridVoltage (V)',
        'Grid L1 Current (A)', 'Grid L1 Voltage (V)', 'Grid L2 Current (A)', 'Grid L2 Voltage (V)',
        'Grid L3 Current (A)',
        'Grid L3 Voltage (V)']
Ambient = ['Outdoor Temp (°C)', 'Outdoor Temperature #1 (°C)', 'Wind Direction #1 (°)', 'Wind Speed #1 (m/s)']
Converter = ['Inv Actual TorqueSP (Nm)', 'Inv Temp Cooling Water Cold (°C)', 'Inv Temp Cooling Water Hot (°C)',
             'Inv Temp HeatSink (°C)', 'Inv Delta Temp Cooling (°C)']
Rotor = ['Rotor Rpm IGR (rpm)', 'Rotor Rpm SafeSys (rpm)', 'Delta Rotor RPM (rpm)']
Yaw = ['Yaw Nacelle pos (°)', 'Yaw Wind Direction 1 (°)', 'Yaw Wind Direction 2 (°)', 'Yaw Wind Speed 100ms (m/s)',
       'Yaw Wind Speed 2 (m/s)']

components_dict = {'PLU 1': PLU_1,
                   'PLU 2': PLU_2,
                   'PLU 3': PLU_3,
                   'Gearbox': Gearbox,
                   'Main Bearing': MainBearing,
                   'Power Reduction': Power_Reduction,
                   'LVU': LVU,
                   'Miscellaneous': Miscellaneous,
                   'Wind Farm Management': Wind_Farm_Management,
                   'Generator': Generator,
                   'Grid': Grid,
                   'Ambient': Ambient,
                   'Converter': Converter,
                   'Rotor': Rotor,
                   'Yaw': Yaw}

buttons = html.Div(
    [
        dbc.Button("Clear Canvas", color="info", id='clear-canvas-button', n_clicks=0, className="mr-1"),
        dbc.Button("Update", id='add-chart', color="danger", n_clicks=0, className="mr-1"),
        # dbc.Button("Export Plots",id='export-plot-button', color="success", n_clicks=0, className="mr-1"),
    ]
)

manual_selection = dbc.FormGroup(
    [
        # dbc.Label("Manual mode selection"),
        dbc.Checklist(
            options=[
                {"label": "Class Mode", "value": 'Class_mode'},
                {"label": "Manual Mode", "value": 'Manual_mode'},
            ],
            value=[],
            id="manual-switches-input",
            switch=True,
        ),
    ]
)
x_axis_drpdwn = dbc.FormGroup(
    [
        dbc.Label("X Axis selection"),
        dbc.Col([
            dbc.Select(
                id="select-x-axis-drpdwn",
                options=[{'label': "Time", 'value': "Time"},
                         {'label': "Wind Speed", 'value': "Wind Speed #1 (m/s)"},
                         {'label': "Generator Power", 'value': "GridRealPower (kW)"},
                         {'label': "Generator Speed", 'value': "Speed Generator (rpm)"},
                         {'label': "Pitch Angle", 'value': "PLU1 Pitch Angle PS1 (°)"}],
                value="Time",
                # style={'width': "100%",},
                bs_size='sm'
            ), ], md=12)
    ],
    row=True,

)

steady_filters = dbc.FormGroup([
    dbc.Label("Steady Condition Filter"),
    dbc.Col(
        dbc.InputGroup(
            [
                dbc.InputGroupAddon("Cons. Points", addon_type="prepend"),
                dbc.Input(type="number",min=1, step=1, id="cons_points_filter"),
                dbc.InputGroupAddon("Dev.", addon_type="prepend"),
                dbc.Input(type="number",min=0.001,step=0.005, id="dev_filter"),
            ],
            # className="mb-3",
            size='sm'
        ), md=12),
], row=True)
text_area = dbc.FormGroup(
    [
        # dbc.Label("Status"),
        dcc.Loading(html.Div(id='textarea',
                             style={'width': '100%', 'height': 100, 'Y-overflow': 'True', 'borderStyle': 'solid',
                                    'borderRadius': '5px', 'background-color': 'gray', 'margin-top': '5px'}))
    ])

col_style = {'border': 'solid', 'align': 'center', 'justify': 'center', 'margin': "0px", 'padding': '20px'}
content = dbc.Row([
    dbc.Row([dbc.Col([Tab1.generate_select_farm_drpdwn(), generate_check_list()], md=2, style=Tab1.style),
             dbc.Col([select_start_date_time, select_end_date_time, manual_selection,
                      class_drpdwn, power, Nacelle_temp, pitch_angle, gend_speed, data_type, steady_filters,x_axis_drpdwn], md=3,
                     style=col_style),
             dbc.Col([component_selection], style=Tab1.style, md=3),
             dbc.Col([html.Div(id='Hidden-Div_trend', children=[0, 0], style={'display': 'none'}),
                      html.Div(sensor_selection, style={'height': '80%'}), buttons, text_area], style=Tab1.style, md=3)
             ], justify='around'),
    html.Div(id='dynamic_callback_container', children=[], style={'margin-top': '15px', 'margin-left': '20px'})
])

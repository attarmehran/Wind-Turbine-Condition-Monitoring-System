from dash.dependencies import Input, Output, State
from app import app
import turbineView.Database_Tools as DBT
import turbineView.Analysis_Tools as AT
import pandas as pd
import numpy


@app.callback(
    [Output('Hidden-Div', 'children'),
     Output('Hidden-Div-production-statistics', 'children'),
     Output('Hidden-Div-windrose', 'children'),
     Output('Hidden-Div-working-class', 'children'),
     Output('gauge-gen-speed', "figure"),
     Output('gauge-gen-power', "figure"),
     Output('bar-temp-comparison', "figure"),
     Output('wind-speed-card', 'children'),
     Output('last_update_id', 'children'),
     Output('today_production', 'children'),
     Output('month_production', 'children'),
     Output('total-production', 'children'),
     Output('turbine_type', 'children'),
     Output('rated_power', 'children'),
     Output('power_setpoint', 'children'),
     Output('today_avail', 'children'),
     Output('month_avail', 'children'),
     Output('total_avail', 'children'),
     Output('uptime', 'children'),
     Output('wind_direction-stats', 'children'),
     Output('turbine-direction-stats', 'children'),
     Output('gap-direction', 'children')
     ],
    [Input('select-turbine', 'value')])
def turbine_view_main(unit):
    df = DBT.read_data(unit)
    hdf_df = AT.stableframe(df)
    power_curve_df = hdf_df[['Wind Speed #1 (m/s)', 'GridRealPower (kW)','Speed Generator (rpm)','PLU1 Pitch Angle PS1 (°)']]
    hdf_dff = power_curve_df.to_json(date_format='iso', orient='split')

    ps_df = AT.collect_production_statistics_data()
    ps_dff = ps_df.to_json(date_format='iso', orient='split')

    windrose_df= hdf_df[['Wind Speed #1 (m/s)','Wind Direction #1 (°)']]
    windrose_dff=windrose_df.to_json(date_format='iso', orient='split')

    working_class_df = hdf_df[['Time','GridRealPower (kW)','PLU1 Pitch Angle PS1 (°)']]
    working_class_dff = working_class_df.to_json(date_format='iso', orient='split')


    comparison_bar = AT.comparison_bar_chart(AT.outdoor_temp(hdf_df)[0], AT.nacelle_temp(hdf_df)[0])

    productivity = AT.productivity(hdf_df, unit)
    last_updated_time = productivity[1]
    today_production = productivity[2]
    month_production = productivity[3]
    total_production = productivity[4]
    uptime = str(productivity[5])

    turbine_type = AT.technical_spec(hdf_df, unit)[1]

    rated_power = AT.technical_spec(hdf_df, unit)[2]
    power_setpoint = AT.technical_spec(hdf_df, unit)[3]

    today_avail = round(AT.availibility(df, unit)[1])
    month_avail = round(AT.availibility(df, unit)[2])
    total_avail = round(AT.availibility(df, unit)[3])
    wind_speed = AT.wind_speed(hdf_df)[0]

    wind_direction = hdf_df['Wind Direction #1 (°)'].iloc[0].astype(int)
    turbine_direction = hdf_df['Yaw Nacelle pos (°)'].iloc[0].astype(float)
    gap_direction = round(abs(wind_direction - turbine_direction),2)
    if numpy.isnan(gap_direction):
        gap_direction = "NAN"

    return hdf_dff, ps_dff,windrose_dff, working_class_dff, AT.gen_speed(hdf_df), AT.gen_power(hdf_df), comparison_bar, wind_speed, \
           last_updated_time, today_production, month_production,total_production, turbine_type, rated_power, power_setpoint,\
           today_avail, month_avail,total_avail,uptime,wind_direction,turbine_direction, gap_direction


@app.callback(
    Output('power-curve-graph', "figure"),
    [Input('Hidden-Div', "children"),
     Input("power-curve-drpdwn", "value"),
     Input("select-turbine", "value")],
)
def power_curve_graph(df, time_period, unit_numb):
    dff = pd.read_json(df, orient='split')
    return AT.power_curve(dff, unit_numb, int(time_period))


@app.callback(
    Output('production-statistics-graph', "figure"),
    [Input('Hidden-Div-production-statistics', "children"),
     Input("production-statistics-drpdwn", "value"),
     ],
)
def production_statistics_graph(df, time_period):
    dff = pd.read_json(df, orient='split')
    return AT.production_statistic(dff, int(time_period))

@app.callback(
    Output('rose-wind', 'figure'),
    [Input('Hidden-Div-windrose', 'children'),
     Input("windrose-drpdwn", "value"),
     ],
)
def production_statistics_graph(df, time_period):
    dff = pd.read_json(df, orient='split')
    return AT.wind_rose(dff, int(time_period))

@app.callback(
    Output('working-class-graph', 'figure'),
    [Input('Hidden-Div-working-class', 'children'),
     Input("working-class-drpdwn", "value"),
     ],
)
def working_class_graph(df, time_period):
    dff = pd.read_json(df, orient='split')
    return AT.class_performance(dff, int(time_period))




card_background_color = '#7F797C'

border_style = {'display': 'flex', 'justify-content': 'center', "border-style": "solid",
                'border-color': '#ff4d4d', 'border-width': '1px', 'border-radius': "0.25rem"
                }


def gen_speed(df):
    """This function calculates the generator speed of a unit"""
    # input:
    # df: coresponding dataframe for the unit
    # output:
    # gen_speed_updated: variable which shows the last value of generator speed from the dataframe
    # last_time_updated: variable which shows the last time of available data

    import plotly.graph_objects as go
    from numpy import mean

    try:
        time = df['Time']
        generator_speed = df['Speed Generator (rpm)']
        ave_gen_speed = mean(generator_speed)

        last_time_updated = time.iloc[0]
        gen_speed_updated = generator_speed.iloc[0]

        fig = go.Figure(go.Indicator(
            domain={'x': [0, 1], 'y': [0, 0.8]},
            value=gen_speed_updated,
            mode="gauge+number+delta",
            title={'text': " Generator Speed (rpm)", 'font': {'size': 16, 'color': 'white'}},
            delta={'reference': 1167},
            gauge={'axis': {'range': [0, 1170]},
                   'steps': [
                       {'range': [0, 1100], 'color': "lightgray"},
                       {'range': [1100, 1167], 'color': "gray"}],
                   'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 1168}}))

        # fig.show()


    except:
        print("No Data To Shown for Generator Speed")

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        # height=160,
        # width=320,
        # padding=dict(l=0, r=0, t=0, b=0),
        margin=dict(l=25, r=35, t=0, b=0),
        font={'color': 'white', 'family': 'Arial, sans-serif'})
    # return gen_speed_updated, last_time_updated
    return fig


def gen_power(df):
    """ This function calculates the generator power for a unit and returns the generator power as gauge curve as well as
    the generator power as an integer value """
    # inputs
    # df: pandas dataframe variable for the corresponding

    from numpy import mean
    import plotly.graph_objects as go

    data = df
    real_power = data['GridRealPower (kW)']
    time = data['Time']

    ave_real_power = mean(real_power)
    real_power_last = real_power.iloc[0]

    fig = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 0.8]},
        value=real_power_last,
        mode="gauge+number+delta",
        title={'text': " Generator Power (KW)", 'font': {'size': 16, 'color': 'white'}},
        delta={'reference': 2500},
        gauge={'axis': {'range': [0, 2520]},
               'steps': [
                   {'range': [2200, 2470], 'color': "lightgray"},
                   {'range': [2470, 2520], 'color': "gray"}],
               'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 2500}}))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        # height=160,
        # width=320,
        # padding=dict(l=0, r=0, t=0, b=0),
        margin=dict(l=25, r=35, t=0, b=0),
        font={'color': 'white', 'family': 'Arial, sans-serif'})

    # fig.show()

    return fig


def wind_speed(df):
    """ This function calculates the wind speed of a unit and returns the wind speed as an integer value as well as
    it returns the wind speed using an indicator from plotly library"""
    import numpy
    # inputs:
    # df: panadas dataframe type - dataframe corresponding to the unit

    wind_speed_last = round(df['Wind Speed #1 (m/s)'].iloc[0], 1)
    if numpy.isnan(wind_speed_last):
        wind_speed_last = 'NAN'
    time_last_update = df['Time'].iloc[0]

    return wind_speed_last, time_last_update


def outdoor_temp(df):
    """ This function calculates the outdoor temperature of a unit and returns the outdoor temperature as an integer value as well as
    it returns the wind speed using an indicator from plotly library"""

    # inputs:
    # df: panadas dataframe type - dataframe corresponding to the unit
    last_time_updated = df['Time'].iloc[0]
    outdoor_temp_updated = df['Outdoor Temp (°C)'].iloc[0]

    return outdoor_temp_updated, last_time_updated


def nacelle_temp(df):
    """ This function calculates the nacelle temperature for a unit and returns the nacelle temperature as an integer value as well as
    it returns the wind speed using an indicator from plotly library"""

    # inputs:
    # df: panadas dataframe type - dataframe corresponding to the unit

    nacelle_temp_last_update = df['Temp Nacelle (°C)'].iloc[0]
    time_last_update = df['Time'].iloc[0]

    return nacelle_temp_last_update, time_last_update


def power_curve(df, unit_num, time_duration):
    """This function calculates the power curve of a unit according to a specific time duration"""
    # inputs:
    # df: pandas dataframe variable for the unit
    # unit_num: this variable shows the unit number - string data type
    # time_duration: variable shows the duration of analysis (filter) - integer data type
    # time_duration = 0: last 24 hours
    # time_duration = 1: last week
    # time_duration = 2: last month
    # time_duration = 3: last 3 months

    import plotly.graph_objects as go
    from pandas import DataFrame
    from trendMonitoringFunctions import steady_condition_filter
    from trendMonitoringFunctions import processed_data
    data = steady_condition_filter(df, 3, 0.2)
    data = processed_data(data)

    wind_speed = data['Wind Speed #1 (m/s)']
    power = data['GridRealPower (kW)']

    d = {'Wind Speed (m/s)': wind_speed, 'Power (KW)': power}
    df = DataFrame(data=d)

    if time_duration == 0:
        wind_speed = df.iloc[0:288, 0]
        power = df.iloc[0:288, 1]
        state = 'Last 24 hours'
    elif time_duration == 1:
        wind_speed = df.iloc[0:288 * 7, 0]
        power = df.iloc[0:288 * 7, 1]
        state = 'Last week'
    elif time_duration == 2:
        wind_speed = df.iloc[0:288 * 30, 0]
        power = df.iloc[0:288 * 30, 1]
        state = 'Last month'
    else:
        wind_speed = df.iloc[0:288 * 90, 0]
        power = df.iloc[0:288 * 90, 1]
        state = 'Last 3 months'

    d_new = {'Wind Speed (m/s)': wind_speed, 'Power (KW)': power}
    df_new = DataFrame(data=d_new)

    trace0 = go.Scattergl(x=wind_speed, y=power, name=state, mode='markers', marker=dict(color='#ff4d4d'))

    trace1 = go.Scattergl(x=[0, 2.5, 5,7.5, 11, 13, 15, 18, 20, 22, 25], y=[0,0, 600, 1250,2530, 2530, 2530, 2530, 2530, 2530,2530],
                        name='Reference', mode='lines', fillcolor='violet', marker=dict(color='#11FF00'))

    data = [trace0, trace1]
    layout = go.Layout(title=" WTG " + unit_num + " - " "Power Curve for " + state, xaxis={'title': 'Wind Speed (m/s)'},
                       yaxis={'title': 'Power (KW)'})
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title={'text': ' Power Curve', 'font': {'size': 20, 'color': 'white', }},
        margin=dict(l=10, r=20, t=20, b=20),
        font={'color': 'white', 'family': 'Arial, sans-serif'},
        xaxis_title="Wind Speed, m/s",
        yaxis_title="Power, kW",
    )
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(
            family="Times New Roman",
            size=14,
            color="white"
        ),
        bordercolor="#ff4d4d",
        borderwidth=2
    ))
    fig.update_xaxes(showgrid=False, showline=False, linewidth=2, linecolor='white')
    fig.update_yaxes(showgrid=False, showline=False, linewidth=2, linecolor='white')

    return fig


def productivity(df, unit_num):
    """This function calculates the productivity variables of a unit - productivity variables consist of:
     {last updated time,
     real power produced by the wind turbine in a day,
     real power produced by the wind turbine in a month} """
    # inputs:
    # df: corresponding dataframe for the unit
    # unit_num: shows the unit number - string data type ex: '01': shows unit number 01

    from pandas import DataFrame
    unit_num = 'WTG ' + str(unit_num)
    data = df
    size = data.shape[0]
    date1 = data.iloc[0,0]
    date2 = data.iloc[size-1,0]
    duration = date1 - date2

    last_updated_time = data['Time'].iloc[0]
    power = data['GridRealPower (kW)']
    power = DataFrame(power)
    try:
        power = power.astype(int)
    except:
        print = 'NAN in productivity card - power production'
    power_production_today = power.iloc[0:288, 0].sum()
    power_production_month = power.iloc[0:288 * 30, 0].sum()
    total_power = power.iloc[:, 0].sum()

    power_production_today = f"{round(power_production_today):,}"
    power_production_month = f"{round(power_production_month):,}"
    total_power = f"{round(total_power):,}"
    productivity_Params = [unit_num, last_updated_time, power_production_today, power_production_month,total_power,duration]
    return productivity_Params


def technical_spec(df, unit_num):
    """ This function calculates the technical specifications of a unit (WTG) and returns a list data type for
     specification parameters of a unit"""

    # imputs:
    # df: dataframe corresponding to the unit
    # unit_num: variable which shows the unit number - string variable
    data = df
    time = data['Time'].iloc[0]
    if unit_num <= '08':
        power_setpoint = data['Active Power Set Point WFM (kW)'].iloc[0]
    else:
        power_setpoint = data['Active Power SetPoint WFM (kW)'].iloc[0]
    rated_power = data['GridRealPower (kW)'].iloc[0]
    turbine_type = 'Fuhrlander - FL2500 KW'
    try:
        power_setpoint = f'{power_setpoint.astype(int):,}'
    except:
        power_setpoint = 'NAN'
    try:
        rated_power = f'{rated_power.astype(int):,}'
    except:
        rated_power = 'NAN'

    technical_spec_Params = [time, turbine_type, rated_power, power_setpoint]
    return technical_spec_Params


def availibility(df, unit_num):
    """ This function calculate the amount of availibility for a unit as percent.
    It returns the following parameters: {
        % availability for today,
        % availability for month"""
    # imputs:
    # df: corresponding dataframe for a unit
    # unit_num: shows the unit number as a string data type
    unit_num = 'WTG ' + str(unit_num)
    data = df
    gen_speed = data[['Speed Generator (rpm)']]
    gen_speed_today = gen_speed.iloc[0:288, 0]
    gen_speed_month = gen_speed.iloc[0:288 * 30, 0]
    total_today = gen_speed_today.shape[0]

    out_of_service_today = gen_speed_today.loc[gen_speed_today <= 100].shape[0]
    at_service_today = total_today - out_of_service_today
    at_service_today_percent = (at_service_today / total_today) * 100
    total_month = gen_speed_month.shape[0]
    out_of_service_month = gen_speed_month.loc[gen_speed_month <= 100].shape[0]
    at_service_month = total_month - out_of_service_month
    at_service_month_percent = (at_service_month / total_month) * 100

    total = gen_speed.shape[0]
    total_out_of_service = gen_speed.loc[gen_speed['Speed Generator (rpm)'] <= 100].shape[0]
    total_at_service = total - total_out_of_service
    total_at_service_percent = round((total_at_service/total) * 100,2)


    avail_Params = [unit_num, at_service_today_percent, at_service_month_percent,total_at_service_percent]
    print(avail_Params)
    return avail_Params


def production_statistic(df, time_duration):
    import plotly.graph_objects as go
    unit_num = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16',
                '17',
                '18', '19', '20', '21', '22']
    if time_duration == 0:
        power01 = df.iloc[0:288, 0].sum()
        power02 = df.iloc[0:288, 1].sum()
        power03 = df.iloc[0:288, 2].sum()
        power04 = df.iloc[0:288, 3].sum()
        power05 = df.iloc[0:288, 4].sum()
        power06 = df.iloc[0:288, 5].sum()
        power07 = df.iloc[0:288, 6].sum()
        power08 = df.iloc[0:288, 7].sum()
        power09 = df.iloc[0:288, 8].sum()
        power10 = df.iloc[0:288, 9].sum()
        power11 = df.iloc[0:288, 10].sum()
        power12 = df.iloc[0:288, 11].sum()
        power13 = df.iloc[0:288, 12].sum()
        power14 = df.iloc[0:288, 13].sum()
        power15 = df.iloc[0:288, 14].sum()
        power16 = df.iloc[0:288, 15].sum()
        power17 = df.iloc[0:288, 16].sum()
        power18 = df.iloc[0:288, 17].sum()
        power19 = df.iloc[0:288, 18].sum()
        power20 = df.iloc[0:288, 19].sum()
        power21 = df.iloc[0:288, 20].sum()
        power22 = df.iloc[0:288, 21].sum()
        state = 'Last 24 hours'

    elif time_duration == 1:
        power01 = df.iloc[0:288 * 7, 0].sum()
        power02 = df.iloc[0:288 * 7, 1].sum()
        power03 = df.iloc[0:288 * 7, 2].sum()
        power04 = df.iloc[0:288 * 7, 3].sum()
        power05 = df.iloc[0:288 * 7, 4].sum()
        power06 = df.iloc[0:288 * 7, 5].sum()
        power07 = df.iloc[0:288 * 7, 6].sum()
        power08 = df.iloc[0:288 * 7, 7].sum()
        power09 = df.iloc[0:288 * 7, 8].sum()
        power10 = df.iloc[0:288 * 7, 9].sum()
        power11 = df.iloc[0:288 * 7, 10].sum()
        power12 = df.iloc[0:288 * 7, 11].sum()
        power13 = df.iloc[0:288 * 7, 12].sum()
        power14 = df.iloc[0:288 * 7, 13].sum()
        power15 = df.iloc[0:288 * 7, 14].sum()
        power16 = df.iloc[0:288 * 7, 15].sum()
        power17 = df.iloc[0:288 * 7, 16].sum()
        power18 = df.iloc[0:288 * 7, 17].sum()
        power19 = df.iloc[0:288 * 7, 18].sum()
        power20 = df.iloc[0:288 * 7, 19].sum()
        power21 = df.iloc[0:288 * 7, 20].sum()
        power22 = df.iloc[0:288 * 7, 21].sum()
        state = 'Last week'

    else:
        state = 'Last month'
        power01 = df.iloc[0:288 * 30, 0].sum()
        power02 = df.iloc[0:288 * 30, 1].sum()
        power03 = df.iloc[0:288 * 30, 2].sum()
        power04 = df.iloc[0:288 * 30, 3].sum()
        power05 = df.iloc[0:288 * 30, 4].sum()
        power06 = df.iloc[0:288 * 30, 5].sum()
        power07 = df.iloc[0:288 * 30, 6].sum()
        power08 = df.iloc[0:288 * 30, 7].sum()
        power09 = df.iloc[0:288 * 30, 8].sum()
        power10 = df.iloc[0:288 * 30, 9].sum()
        power11 = df.iloc[0:288 * 30, 10].sum()
        power12 = df.iloc[0:288 * 30, 11].sum()
        power13 = df.iloc[0:288 * 30, 12].sum()
        power14 = df.iloc[0:288 * 30, 13].sum()
        power15 = df.iloc[0:288 * 30, 14].sum()
        power16 = df.iloc[0:288 * 30, 15].sum()
        power17 = df.iloc[0:288 * 30, 16].sum()
        power18 = df.iloc[0:288 * 30, 17].sum()
        power19 = df.iloc[0:288 * 30, 18].sum()
        power20 = df.iloc[0:288 * 30, 19].sum()
        power21 = df.iloc[0:288 * 30, 20].sum()
        power22 = df.iloc[0:288 * 30, 21].sum()

    fig = go.Figure(data=[
        go.Bar(marker_color='#ff4d4d',
               name='Measured value', x=unit_num,
               y=[power01, power02, power03, power04, power05, power06, power07, power08,
                  power09, power10, power11, power12, power13, power14, power15, power16,
                  power17, power18, power19, power20, power21, power22]),
        go.Bar(marker_color=card_background_color,
               name='Expected value', x=unit_num,
               y=[(2500 * 288 * 7) - power01, (2500 * 288 * 7) - power02, (2500 * 288 * 7) - power03,
                  (2500 * 288 * 7) - power04, (2500 * 288 * 7) - power05, (2500 * 288 * 7) - power06,
                  (2500 * 288 * 7) - power07, (2500 * 288 * 7) - power08, (2500 * 288 * 7) - power09,
                  (2500 * 288 * 7) - power10, (2500 * 288 * 7) - power11, (2500 * 288 * 7) - power12,
                  (2500 * 288 * 7) - power13,
                  (2500 * 288 * 7) - power14, (2500 * 288 * 7) - power15, (2500 * 288 * 7) - power16,
                  (2500 * 288 * 7) - power17, (2500 * 288 * 7) - power18, (2500 * 288 * 7) - power19,
                  (2500 * 288 * 7) - power20, (2500 * 288 * 7) - power21, (2500 * 288 * 7) - power22])
    ])
    fig.update_layout(title="Production Statistics " + "for " + state, barmode='stack',
                      xaxis={'title': 'Units', 'categoryarray': unit_num}, yaxis={'title': 'Power (KW)'},
                      )  # xaxis_tickfont_size=8

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title={'text': ' Production Statistics', 'font': {'size': 20, 'color': 'white', }},
        margin=dict(l=10, r=20, t=20, b=20),
        font={'color': 'white', 'family': 'Arial, sans-serif'},
        xaxis_title="Unit Number",
        yaxis_title="Power, kW",
    )
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(
            family="Times New Roman",
            size=14,
            color="white"
        ),
        bordercolor="#ff4d4d",
        borderwidth=2
    ))
    fig.update_xaxes(nticks=len(unit_num), dtick=1)
    fig.update_xaxes(showgrid=False, showline=False, linewidth=2, linecolor='white')
    fig.update_yaxes(showgrid=False, showline=False, linewidth=2, linecolor='white')

    return fig


def collect_production_statistics_data():
    from turbineView.Database_Tools import read_data
    import pandas as pd
    unit_num = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
                '18', '19', '20', '21', '22']
    df = pd.DataFrame()
    for i in unit_num:
        data = read_data(i)
        power = data['GridRealPower (kW)']
        power = pd.DataFrame(power)
        power.reset_index(inplace=True, drop=True)
        df = pd.concat([df, power], axis=1)

    return df


def service_availability(unit_num, start_date, end_date):
    """This function """
    from turbineView.Database_Tools import read_data
    from turbineView.Database_Tools import datetime_filter
    from pandas import DataFrame
    import plotly.graph_objects as go

    df = read_data(unit_num)
    time = df['Time']
    gen_speed = df['Speed Generator (rpm)']

    columns = {'Time': time, 'Speed Generator (rpm)': gen_speed}
    df = DataFrame(columns)
    df = datetime_filter(df, start_date, end_date)
    at_service = df.shape[0]
    out_of_service = df.loc[df['Speed Generator (rpm)'] <= 100].shape[0]

    labels = ['At Service', 'Out of Service']
    values = [at_service, out_of_service]

    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    labels = ["At Service", "Out of Service"]

    # Create subplots: use 'domain' type for Pie subplot
    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
    fig.add_trace(go.Pie(labels=labels, values=[at_service, out_of_service], name="Unit Availability"),
                  1, 1)

    # Use `hole` to create a donut-like pie chart
    fig.update_traces(hole=.4, hoverinfo="label+percent+name")

    fig.update_layout(
        title_text="WTG " + str("01") + " Availability",
        # Add annotations in the center of the donut pies.
        annotations=[dict(text='', x=0.18, y=0.5, font_size=20, showarrow=False),
                     ])
    fig.show()

    return


def comparison_bar_chart(outdoor_temp, nacelle_temp):
    import plotly.graph_objects as go

    x_axis = [outdoor_temp, nacelle_temp]
    y_axis = ['Outdoor Temp', 'Nacelle Temp']
    fig = go.Figure(data=[go.Bar(x=y_axis, y=x_axis, marker_color='#ff4d4d')])
    fig.update_layout(
        yaxis_title="Temperature °C",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=30, t=20, b=20),
        font={'color': 'white', 'family': 'Arial, sans-serif'})
    fig.update_xaxes(showgrid=False, showline=False, linewidth=2, linecolor='black')
    fig.update_yaxes(showgrid=False, showline=False, linewidth=2, linecolor='black')
    return fig


def live_data(df, unit_num):
    """ This function produces the live data for the farm view panel"""
    import random
    from pandas import DataFrame
    unit_num = 'WTG ' + str(unit_num)
    last_time = df['Time'].iloc[0]
    gen_speed = df['Speed Generator (rpm)'].iloc[0]
    power = df['GridRealPower (kW)']
    output_power = df['GridRealPower (kW)'].iloc[0]
    wind_speed = df['Wind Speed #1 (m/s)'].iloc[0]
    wind_speed = round(wind_speed, 1)
    power_today = power.iloc[0:288]
    total_power_today = power_today.sum()
    alarm_code = 'Normal'
    condition = random.randint(0, 5)

    live_Params = {'Name': unit_num,
                   'Last Update Time': last_time,
                   'Output Power (KW)': output_power,
                   'Total Production Today (KWh)': total_power_today,
                   'Generator Speed (rpm)': gen_speed,
                   'Wind Speed (m/s)': wind_speed,
                   'Alarm Code Status': alarm_code,
                   }
    df_new = DataFrame([live_Params])

    col_name0 = 'Name'
    col_name1 = "Last Update Time"
    col_name2 = 'Total Production Today (KWh)'
    col_name3 = 'Output Power (KW)'
    col_name4 = 'Generator Speed (rpm)'
    col_name5 = 'Wind Speed (m/s)'

    zero_col = df_new.pop(col_name0)
    first_col = df_new.pop(col_name1)
    second_col = df_new.pop(col_name2)
    third_col = df_new.pop(col_name3)
    forth_col = df_new.pop(col_name4)
    fifth_col = df_new.pop(col_name5)

    df_new.insert(0, col_name0, zero_col)
    df_new.insert(1, col_name1, first_col)
    df_new.insert(2, col_name2, second_col)
    df_new.insert(3, col_name3, third_col)
    df_new.insert(4, col_name4, forth_col)
    df_new.insert(5, col_name5, fifth_col)

    df_new.reset_index(drop=True, inplace=True)
    return df_new


def generate_hdf_live_data():
    from turbineView.Database_Tools import read_data
    from pandas import DataFrame
    from pandas import concat

    df = DataFrame()
    for i in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
              '18', '19', '20', '21', '22']:
        df_new = read_data(i)
        data = live_data(df_new, i)
        df = concat([df, data], axis=0)

    df.to_hdf('./Kahak/livedataTable', key='df', mode='w')


def wind_rose(df, time_duration):
    import plotly.graph_objects as go
    from pandas import DataFrame

    wind_speed = df['Wind Speed #1 (m/s)']
    wind_direction = df['Wind Direction #1 (°)']

    d = {'Wind Speed #1 (m/s)': wind_speed, 'Wind Direction #1 (°)': wind_direction}
    df = DataFrame(data=d)

    if time_duration == 0:
        df = df.iloc[0:288, :]
    elif time_duration == 1:
        df = df.iloc[0:288 * 7, :]
    elif time_duration == 2:
        df = df.iloc[0:288 * 30, :]
    else:
        df = df.iloc[0:288 * 30 * 6, :]

    r11 = df.loc[(df['Wind Speed #1 (m/s)'] > 0) & (df['Wind Speed #1 (m/s)'] < 5) &
                 (df['Wind Direction #1 (°)'] >= 0) & (df['Wind Direction #1 (°)'] < 30)].shape[0]

    r12 = df.loc[(df['Wind Speed #1 (m/s)'] > 0) & (df['Wind Speed #1 (m/s)'] < 5) &
                 (df['Wind Direction #1 (°)'] >= 30) & (df['Wind Direction #1 (°)'] < 60)].shape[0]

    r13 = df.loc[(df['Wind Speed #1 (m/s)'] > 0) & (df['Wind Speed #1 (m/s)'] < 5) &
                 (df['Wind Direction #1 (°)'] >= 60) & (df['Wind Direction #1 (°)'] < 90)].shape[0]

    r14 = df.loc[(df['Wind Speed #1 (m/s)'] > 0) & (df['Wind Speed #1 (m/s)'] < 5) &
                 (df['Wind Direction #1 (°)'] >= 90) & (df['Wind Direction #1 (°)'] < 120)].shape[0]

    r15 = df.loc[(df['Wind Speed #1 (m/s)'] > 0) & (df['Wind Speed #1 (m/s)'] < 5) &
                 (df['Wind Direction #1 (°)'] >= 120) & (df['Wind Direction #1 (°)'] < 150)].shape[0]

    r16 = df.loc[(df['Wind Speed #1 (m/s)'] > 0) & (df['Wind Speed #1 (m/s)'] < 5) &
                 (df['Wind Direction #1 (°)'] >= 150) & (df['Wind Direction #1 (°)'] < 180)].shape[0]

    r17 = df.loc[(df['Wind Speed #1 (m/s)'] > 0) & (df['Wind Speed #1 (m/s)'] < 5) &
                 (df['Wind Direction #1 (°)'] >= 180) & (df['Wind Direction #1 (°)'] < 210)].shape[0]

    r18 = df.loc[(df['Wind Speed #1 (m/s)'] > 0) & (df['Wind Speed #1 (m/s)'] < 5) &
                 (df['Wind Direction #1 (°)'] >= 210) & (df['Wind Direction #1 (°)'] < 240)].shape[0]

    r19 = df.loc[(df['Wind Speed #1 (m/s)'] > 0) & (df['Wind Speed #1 (m/s)'] < 5) &
                 (df['Wind Direction #1 (°)'] >= 240) & (df['Wind Direction #1 (°)'] < 270)].shape[0]

    r110 = df.loc[(df['Wind Speed #1 (m/s)'] > 0) & (df['Wind Speed #1 (m/s)'] < 5) &
                  (df['Wind Direction #1 (°)'] >= 270) & (df['Wind Direction #1 (°)'] < 300)].shape[0]

    r111 = df.loc[(df['Wind Speed #1 (m/s)'] > 0) & (df['Wind Speed #1 (m/s)'] < 5) &
                  (df['Wind Direction #1 (°)'] >= 300) & (df['Wind Direction #1 (°)'] < 330)].shape[0]

    r112 = df.loc[(df['Wind Speed #1 (m/s)'] > 0) & (df['Wind Speed #1 (m/s)'] < 5) &
                  (df['Wind Direction #1 (°)'] >= 330) & (df['Wind Direction #1 (°)'] < 360)].shape[0]

    r21 = df.loc[(df['Wind Speed #1 (m/s)'] >= 5) & (df['Wind Speed #1 (m/s)'] < 10) &
                 (df['Wind Direction #1 (°)'] >= 0) & (df['Wind Direction #1 (°)'] < 30)].shape[0]

    r22 = df.loc[(df['Wind Speed #1 (m/s)'] >= 5) & (df['Wind Speed #1 (m/s)'] < 10) &
                 (df['Wind Direction #1 (°)'] >= 30) & (df['Wind Direction #1 (°)'] < 60)].shape[0]

    r23 = df.loc[(df['Wind Speed #1 (m/s)'] >= 5) & (df['Wind Speed #1 (m/s)'] < 10) &
                 (df['Wind Direction #1 (°)'] >= 60) & (df['Wind Direction #1 (°)'] < 90)].shape[0]

    r24 = df.loc[(df['Wind Speed #1 (m/s)'] >= 5) & (df['Wind Speed #1 (m/s)'] < 10) &
                 (df['Wind Direction #1 (°)'] >= 90) & (df['Wind Direction #1 (°)'] < 120)].shape[0]

    r25 = df.loc[(df['Wind Speed #1 (m/s)'] >= 5) & (df['Wind Speed #1 (m/s)'] < 10) &
                 (df['Wind Direction #1 (°)'] >= 120) & (df['Wind Direction #1 (°)'] < 1100)].shape[0]

    r26 = df.loc[(df['Wind Speed #1 (m/s)'] >= 5) & (df['Wind Speed #1 (m/s)'] < 10) &
                 (df['Wind Direction #1 (°)'] >= 1100) & (df['Wind Direction #1 (°)'] < 180)].shape[0]

    r27 = df.loc[(df['Wind Speed #1 (m/s)'] >= 5) & (df['Wind Speed #1 (m/s)'] < 10) &
                 (df['Wind Direction #1 (°)'] >= 180) & (df['Wind Direction #1 (°)'] < 210)].shape[0]

    r28 = df.loc[(df['Wind Speed #1 (m/s)'] >= 5) & (df['Wind Speed #1 (m/s)'] < 10) &
                 (df['Wind Direction #1 (°)'] >= 210) & (df['Wind Direction #1 (°)'] < 240)].shape[0]

    r29 = df.loc[(df['Wind Speed #1 (m/s)'] >= 5) & (df['Wind Speed #1 (m/s)'] < 10) &
                 (df['Wind Direction #1 (°)'] >= 240) & (df['Wind Direction #1 (°)'] < 270)].shape[0]

    r210 = df.loc[(df['Wind Speed #1 (m/s)'] >= 5) & (df['Wind Speed #1 (m/s)'] < 10) &
                  (df['Wind Direction #1 (°)'] >= 270) & (df['Wind Direction #1 (°)'] < 300)].shape[0]

    r211 = df.loc[(df['Wind Speed #1 (m/s)'] >= 5) & (df['Wind Speed #1 (m/s)'] < 10) &
                  (df['Wind Direction #1 (°)'] >= 300) & (df['Wind Direction #1 (°)'] < 330)].shape[0]

    r212 = df.loc[(df['Wind Speed #1 (m/s)'] >= 5) & (df['Wind Speed #1 (m/s)'] < 10) &
                  (df['Wind Direction #1 (°)'] >= 330) & (df['Wind Direction #1 (°)'] < 360)].shape[0]

    r31 = df.loc[(df['Wind Speed #1 (m/s)'] >= 10) & (df['Wind Speed #1 (m/s)'] < 15) &
                 (df['Wind Direction #1 (°)'] > 0) & (df['Wind Direction #1 (°)'] < 30)].shape[0]

    r32 = df.loc[(df['Wind Speed #1 (m/s)'] >= 10) & (df['Wind Speed #1 (m/s)'] < 15) &
                 (df['Wind Direction #1 (°)'] >= 30) & (df['Wind Direction #1 (°)'] < 60)].shape[0]

    r33 = df.loc[(df['Wind Speed #1 (m/s)'] >= 10) & (df['Wind Speed #1 (m/s)'] < 15) &
                 (df['Wind Direction #1 (°)'] >= 60) & (df['Wind Direction #1 (°)'] < 90)].shape[0]

    r34 = df.loc[(df['Wind Speed #1 (m/s)'] >= 10) & (df['Wind Speed #1 (m/s)'] < 15) &
                 (df['Wind Direction #1 (°)'] >= 90) & (df['Wind Direction #1 (°)'] < 120)].shape[0]

    r35 = df.loc[(df['Wind Speed #1 (m/s)'] >= 10) & (df['Wind Speed #1 (m/s)'] < 15) &
                 (df['Wind Direction #1 (°)'] >= 120) & (df['Wind Direction #1 (°)'] < 150)].shape[0]

    r36 = df.loc[(df['Wind Speed #1 (m/s)'] >= 10) & (df['Wind Speed #1 (m/s)'] < 15) &
                 (df['Wind Direction #1 (°)'] >= 150) & (df['Wind Direction #1 (°)'] < 180)].shape[0]

    r37 = df.loc[(df['Wind Speed #1 (m/s)'] >= 10) & (df['Wind Speed #1 (m/s)'] < 15) &
                 (df['Wind Direction #1 (°)'] >= 180) & (df['Wind Direction #1 (°)'] < 210)].shape[0]

    r38 = df.loc[(df['Wind Speed #1 (m/s)'] >= 10) & (df['Wind Speed #1 (m/s)'] < 15) &
                 (df['Wind Direction #1 (°)'] >= 210) & (df['Wind Direction #1 (°)'] < 240)].shape[0]

    r39 = df.loc[(df['Wind Speed #1 (m/s)'] >= 10) & (df['Wind Speed #1 (m/s)'] < 15) &
                 (df['Wind Direction #1 (°)'] >= 240) & (df['Wind Direction #1 (°)'] < 270)].shape[0]

    r310 = df.loc[(df['Wind Speed #1 (m/s)'] >= 10) & (df['Wind Speed #1 (m/s)'] < 15) &
                  (df['Wind Direction #1 (°)'] >= 270) & (df['Wind Direction #1 (°)'] < 300)].shape[0]

    r311 = df.loc[(df['Wind Speed #1 (m/s)'] >= 10) & (df['Wind Speed #1 (m/s)'] < 15) &
                  (df['Wind Direction #1 (°)'] >= 300) & (df['Wind Direction #1 (°)'] < 330)].shape[0]

    r312 = df.loc[(df['Wind Speed #1 (m/s)'] >= 10) & (df['Wind Speed #1 (m/s)'] < 15) &
                  (df['Wind Direction #1 (°)'] >= 330) & (df['Wind Direction #1 (°)'] < 360)].shape[0]

    r41 = df.loc[(df['Wind Speed #1 (m/s)'] >= 15) & (df['Wind Speed #1 (m/s)'] < 20) &
                 (df['Wind Direction #1 (°)'] >= 0) & (df['Wind Direction #1 (°)'] < 30)].shape[0]

    r42 = df.loc[(df['Wind Speed #1 (m/s)'] >= 15) & (df['Wind Speed #1 (m/s)'] < 20) &
                 (df['Wind Direction #1 (°)'] >= 30) & (df['Wind Direction #1 (°)'] < 60)].shape[0]

    r43 = df.loc[(df['Wind Speed #1 (m/s)'] >= 15) & (df['Wind Speed #1 (m/s)'] < 20) &
                 (df['Wind Direction #1 (°)'] >= 60) & (df['Wind Direction #1 (°)'] < 90)].shape[0]

    r44 = df.loc[(df['Wind Speed #1 (m/s)'] >= 15) & (df['Wind Speed #1 (m/s)'] < 20) &
                 (df['Wind Direction #1 (°)'] >= 90) & (df['Wind Direction #1 (°)'] < 120)].shape[0]

    r45 = df.loc[(df['Wind Speed #1 (m/s)'] >= 15) & (df['Wind Speed #1 (m/s)'] < 20) &
                 (df['Wind Direction #1 (°)'] >= 120) & (df['Wind Direction #1 (°)'] < 150)].shape[0]

    r46 = df.loc[(df['Wind Speed #1 (m/s)'] >= 15) & (df['Wind Speed #1 (m/s)'] < 20) &
                 (df['Wind Direction #1 (°)'] >= 150) & (df['Wind Direction #1 (°)'] < 180)].shape[0]

    r47 = df.loc[(df['Wind Speed #1 (m/s)'] >= 15) & (df['Wind Speed #1 (m/s)'] < 20) &
                 (df['Wind Direction #1 (°)'] >= 180) & (df['Wind Direction #1 (°)'] < 210)].shape[0]

    r48 = df.loc[(df['Wind Speed #1 (m/s)'] >= 15) & (df['Wind Speed #1 (m/s)'] < 20) &
                 (df['Wind Direction #1 (°)'] >= 210) & (df['Wind Direction #1 (°)'] < 240)].shape[0]

    r49 = df.loc[(df['Wind Speed #1 (m/s)'] >= 15) & (df['Wind Speed #1 (m/s)'] < 20) &
                 (df['Wind Direction #1 (°)'] >= 240) & (df['Wind Direction #1 (°)'] < 270)].shape[0]

    r410 = df.loc[(df['Wind Speed #1 (m/s)'] >= 15) & (df['Wind Speed #1 (m/s)'] < 20) &
                  (df['Wind Direction #1 (°)'] >= 270) & (df['Wind Direction #1 (°)'] < 300)].shape[0]

    r411 = df.loc[(df['Wind Speed #1 (m/s)'] >= 15) & (df['Wind Speed #1 (m/s)'] < 20) &
                  (df['Wind Direction #1 (°)'] >= 300) & (df['Wind Direction #1 (°)'] < 330)].shape[0]

    r412 = df.loc[(df['Wind Speed #1 (m/s)'] >= 15) & (df['Wind Speed #1 (m/s)'] < 20) &
                  (df['Wind Direction #1 (°)'] >= 330) & (df['Wind Direction #1 (°)'] < 360)].shape[0]

    r51 = df.loc[(df['Wind Speed #1 (m/s)'] >= 20) & (df['Wind Speed #1 (m/s)'] < 25) &
                 (df['Wind Direction #1 (°)'] >= 0) & (df['Wind Direction #1 (°)'] < 30)].shape[0]

    r52 = df.loc[(df['Wind Speed #1 (m/s)'] >= 20) & (df['Wind Speed #1 (m/s)'] < 25) &
                 (df['Wind Direction #1 (°)'] >= 30) & (df['Wind Direction #1 (°)'] < 60)].shape[0]

    r53 = df.loc[(df['Wind Speed #1 (m/s)'] >= 20) & (df['Wind Speed #1 (m/s)'] < 25) &
                 (df['Wind Direction #1 (°)'] >= 60) & (df['Wind Direction #1 (°)'] < 90)].shape[0]

    r54 = df.loc[(df['Wind Speed #1 (m/s)'] >= 20) & (df['Wind Speed #1 (m/s)'] < 25) &
                 (df['Wind Direction #1 (°)'] >= 90) & (df['Wind Direction #1 (°)'] < 120)].shape[0]

    r55 = df.loc[(df['Wind Speed #1 (m/s)'] >= 20) & (df['Wind Speed #1 (m/s)'] < 25) &
                 (df['Wind Direction #1 (°)'] > 120) & (df['Wind Direction #1 (°)'] < 150)].shape[0]

    r56 = df.loc[(df['Wind Speed #1 (m/s)'] >= 20) & (df['Wind Speed #1 (m/s)'] < 25) &
                 (df['Wind Direction #1 (°)'] >= 150) & (df['Wind Direction #1 (°)'] < 180)].shape[0]

    r57 = df.loc[(df['Wind Speed #1 (m/s)'] >= 20) & (df['Wind Speed #1 (m/s)'] < 25) &
                 (df['Wind Direction #1 (°)'] > 180) & (df['Wind Direction #1 (°)'] < 210)].shape[0]

    r58 = df.loc[(df['Wind Speed #1 (m/s)'] >= 20) & (df['Wind Speed #1 (m/s)'] < 25) &
                 (df['Wind Direction #1 (°)'] >= 210) & (df['Wind Direction #1 (°)'] < 240)].shape[0]

    r59 = df.loc[(df['Wind Speed #1 (m/s)'] >= 20) & (df['Wind Speed #1 (m/s)'] < 25) &
                 (df['Wind Direction #1 (°)'] > 240) & (df['Wind Direction #1 (°)'] < 270)].shape[0]

    r510 = df.loc[(df['Wind Speed #1 (m/s)'] >= 20) & (df['Wind Speed #1 (m/s)'] < 25) &
                  (df['Wind Direction #1 (°)'] >= 270) & (df['Wind Direction #1 (°)'] < 300)].shape[0]

    r511 = df.loc[(df['Wind Speed #1 (m/s)'] >= 20) & (df['Wind Speed #1 (m/s)'] < 25) & (
            df['Wind Direction #1 (°)'] > 300) & (df['Wind Direction #1 (°)'] < 330)].shape[0]

    r512 = df.loc[(df['Wind Speed #1 (m/s)'] >= 20) & (df['Wind Speed #1 (m/s)'] < 25) &
                  (df['Wind Direction #1 (°)'] >= 330) & (df['Wind Direction #1 (°)'] < 360)].shape[0]

    fig = go.Figure()

    fig.add_trace(go.Barpolar(
        r=[r11, r12, r13, r14, r15, r16, r17, r18, r19, r110, r111, r112],
        name='5m/s <',
        marker_color='rgb(120,140,247)'
    ))

    fig.add_trace(go.Barpolar(
        r=[r21, r22, r23, r24, r25, r26, r27, r28, r29, r210, r211, r212],
        name='5m/s ~ 10m/s',
        marker_color='rgb(0,0,255)'
    ))
    fig.add_trace(go.Barpolar(
        r=[r31, r32, r33, r34, r35, r36, r37, r38, r39, r310, r311, r312],
        name='10m/s ~ 15m/s',
        marker_color='rgb(128,255,0)'
    ))

    fig.add_trace(go.Barpolar(
        r=[r41, r42, r43, r44, r45, r46, r47, r48, r49, r410, r411, r412],
        name='15m/s ~ 20 m/s',
        marker_color='rgb(204,0,204)'
    ))

    fig.add_trace(go.Barpolar(
        r=[r51, r52, r53, r54, r55, r56, r57, r58, r59, r510, r511, r512],
        name='20m/s ~ 25 m/s',
        marker_color='rgb(238, 26, 26)'
    ))

    fig.update_traces(text=['0 - 30'])
    fig.update_layout(title={'text': ' Local Wind Rose ', 'font': {'size': 20, 'color': 'white', }},
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      legend_font_size=20,
                      font_size=12, font_color='#ff4d4d',
                      polar_radialaxis_ticksuffix=None,
                      polar_angularaxis_rotation=0

                      )

    fig.update_layout(
        legend=dict(

            traceorder="reversed",
            title_font_family="Times New Roman",
            font=dict(
                family="Times New Roman",
                size=14,
                color="white"
            ),
            # bgcolor="LightSteelBlue",
            bordercolor="#ff4d4d",
            borderwidth=2
        )
    )
    return fig


def generate_live_data_table(farm_name, checklist_value):
    from pandas import read_hdf
    import dash_table

    df = read_hdf("./{}/livedataTable".format(farm_name))

    df['Total Production Today (KWh)'] = df['Total Production Today (KWh)'].astype(int).apply(lambda x: f'{x:,}')
    df['Generator Speed (rpm)'] = df['Generator Speed (rpm)'].astype(int).apply(lambda x: f'{x:,}')
    df['Output Power (KW)'] = df['Output Power (KW)'].astype(int).apply(lambda x: f'{x:,}')

    dff = df[df['Name'].isin(checklist_value)]
    dff['Status'] = dff['Alarm Code Status'].apply(lambda x: '✅' if x == 'Normal' else '🔴' if x == 2 else '')
    dataTable = dash_table.DataTable(
        data=dff.to_dict('records'),
        # sort_action='native',
        style_header={
            'backgroundColor': 'rgb(30, 30, 30)',
            'fontWeight': 'bold'
        },
        style_cell={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white',
            'textAlign': 'center'
        },

        fixed_rows={'headers': True, 'data': 0},
        page_action='none',
        style_table={'height': '300px', 'overflowY': 'auto'},
        columns=[{'name': i, 'id': i} for i in dff.columns],
        editable=False,

        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(40, 60, 50)'
            }
        ],
        style_cell_conditional=([
            {'if': {'column_id': 'Name'},
             'width': '6%'},
            {'if': {'column_id': 'Last Update Time'},
             'width': '13%'},
            {'if': {'column_id': 'Total Production Today (KWh)'},
             'width': '18%'},
            {'if': {'column_id': 'Alarm Code Status'},
             'width': '12%'},
            {'if': {'column_id': 'Status'},
             'width': '5%'},
            {'if': {'column_id': 'Output Power (KW)'},
             'width': '12%'},
        ]

        )

    )
    return dataTable


def gen_time_period_drpdown(id):
    import dash_bootstrap_components as dbc
    select = dbc.Select(
        id=id,
        options=[
            {"label": "Last Day", "value": 0},
            {"label": "Last Week", "value": 1},
            {"label": "Last Month", "value": 2},
            {"label": "Last 3 Months", "value": 3},
        ],
        value=1,
        style={'width': "35%"}
    )
    return select


####################################################################################################
def class_01(df):
    df_class01 = df.loc[(df['PLU1 Pitch Angle PS1 (°)'] <= 0.5) & (df['PLU1 Pitch Angle PS1 (°)'] >= -0.5) &
                        (df['GridRealPower (kW)'] >= 2200) & (df['GridRealPower (kW)'] <= 2470)]
    df_class01 = df_class01.sort_values(by=['Time'], ascending=False)
    col_name = "Time"
    first_col = df_class01.pop(col_name)
    df_class01.insert(0, col_name, first_col)
    return df_class01


def class_02(df):
    df_class02 = df.loc[(df['PLU1 Pitch Angle PS1 (°)'] < 7) & (df['PLU1 Pitch Angle PS1 (°)'] > 0.5) &
                        (df['GridRealPower (kW)'] > 2470) & (df['GridRealPower (kW)'] <= 2600)]
    df_class02 = df_class02.sort_values(by=['Time'], ascending=False)
    col_name = "Time"
    first_col = df_class02.pop(col_name)
    df_class02.insert(0, col_name, first_col)
    return df_class02


def class_03(df):
    df_class03 = df.loc[(df['PLU1 Pitch Angle PS1 (°)'] <= 30) & (df['PLU1 Pitch Angle PS1 (°)'] >= 7) &
                        (df['GridRealPower (kW)'] > 2470) & (df['GridRealPower (kW)'] <= 2600)]
    df_class03 = df_class03.sort_values(by=['Time'], ascending=False)
    col_name = "Time"
    first_col = df_class03.pop(col_name)
    df_class03.insert(0, col_name, first_col)
    return df_class03


def class_04(df):
    df_class04 = df.loc[(df['PLU1 Pitch Angle PS1 (°)'] <= 0.5) & (df['PLU1 Pitch Angle PS1 (°)'] >= -0.5) &
                        (df['GridRealPower (kW)'] < 2200)]
    df_class04 = df_class04.sort_values(by=['Time'], ascending=False)
    col_name = "Time"
    first_col = df_class04.pop(col_name)
    df_class04.insert(0, col_name, first_col)
    return df_class04


def class_performance(df, time_duration):
    import plotly.graph_objects as go
    if time_duration == 0:
        df = df.iloc[0:288, :]
        state = 'Last 24 hours'
        shape_class_01 = class_01(df).shape[0]
        shape_class_02 = class_02(df).shape[0]
        shape_class_03 = class_03(df).shape[0]
        shape_class_04 = class_04(df).shape[0]
    elif time_duration == 1:
        df = df.iloc[0:288 * 7, :]
        state = 'Last week'
        shape_class_01 = class_01(df).shape[0]
        shape_class_02 = class_02(df).shape[0]
        shape_class_03 = class_03(df).shape[0]
        shape_class_04 = class_04(df).shape[0]
    elif time_duration == 2:
        df = df.iloc[0:288 * 30, :]
        state = 'Last month'
        total_shape = df.shape[0]
        shape_class_01 = class_01(df).shape[0]
        shape_class_02 = class_02(df).shape[0]
        shape_class_03 = class_03(df).shape[0]
        shape_class_04 = class_04(df).shape[0]
    else:
        df = df.iloc[0:288 * 90, :]
        state = 'Last 3 months'
        total_shape = df.shape[0]
        shape_class_01 = class_01(df).shape[0]
        shape_class_02 = class_02(df).shape[0]
        shape_class_03 = class_03(df).shape[0]
        shape_class_04 = class_04(df).shape[0]

    labels = ['Class 01: pitch angle = 0, 2200 < power < 2470', 'Class 02: 0 < pitch angle < 7, 2470 < power',
              'Class 03: 7 < pitch angle < 30, power > 2470', 'Class 04: power < 2200']
    values = [shape_class_01, shape_class_02, shape_class_03, shape_class_04]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4)])

    fig.update_layout(title={'text': ' Working Class Categories ', 'font': {'size': 20, 'color': 'white', }},
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      legend_font_size=20,
                      font_size=12, font_color='#ff4d4d',
                      polar_radialaxis_ticksuffix=None,
                      polar_angularaxis_rotation=0

                      )

    fig.update_layout(
        legend=dict(
            # x=0,
            # y=1,
            traceorder="reversed",
            title_font_family="Times New Roman",
            font=dict(
                family="Times New Roman",
                size=14,
                color="white"
            ),
            # bgcolor="LightSteelBlue",
            bordercolor="#ff4d4d",
            borderwidth=2
        )
    )

    return fig


def stableframe(df):
    df = df.dropna(how='all')
    df.drop(df[(df['GridRealPower (kW)'] < 0)].index, inplace=True)
    df.drop(df[(df['GridRealPower (kW)'] > 0) & (df['Wind Speed #1 (m/s)'] < 1)].index, inplace=True)
    df.drop(df[(df['PLU1 Pitch Angle PS1 (°)'] < 0.5) & (df['Wind Speed #1 (m/s)'] > 12)].index, inplace=True)

    df.drop(df[df['Speed Generator (rpm)'].diff(periods=3) >= 0.02 * (df['Speed Generator (rpm)'])].index, inplace=True)
    # df = df.set_index('Time','Speed Generator (rpm)').rolling(5).median()

    return df

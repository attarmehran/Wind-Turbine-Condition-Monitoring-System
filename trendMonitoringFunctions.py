import plotly.graph_objects as go


def startup_graph_generation():
    fig = go.Figure()
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=50, b=20),
        font={'color': 'white', 'family': 'Arial, sans-serif'},

    )
    fig.update_layout(legend=dict(
        orientation="h",
        # yanchor="bottom",
        y=-0.3,
        # xanchor="right",
        # x=1,
        font=dict(
            family="Times New Roman",
            size=14,
            color="white"
        ),
        bordercolor="#ff4d4d",
        borderwidth=2
    ))
    fig.update_xaxes(showgrid=False, showline=True, zeroline=False, linewidth=2, linecolor='white')
    fig.update_yaxes(showgrid=False, showline=True, zeroline=False, linewidth=2, linecolor='white')
    return fig

# min_power=-1000, max_power=3000, min_genspeed=-100, max_genspeed=2000, min_angle=-0.5,
#                           max_angle=360,
#                           min_temp=0, max_temp=100
def manual_mode_selection(df, min_power, max_power, min_genspeed, max_genspeed, min_angle,max_angle,min_temp, max_temp):
    filtered_df =df
    if not min_power and not max_power:
        pass
    else:
        filtered_df = filtered_df.loc[(filtered_df['GridRealPower (kW)'] >= min_power) &
                         (filtered_df['GridRealPower (kW)'] <= max_power)]

    if not min_angle and not max_angle:
        pass
    else:
        filtered_df = filtered_df.loc[(filtered_df['PLU1 Pitch Angle PS1 (°)'] >= min_angle) &
                                  (filtered_df['PLU1 Pitch Angle PS1 (°)'] <= max_angle)]
    if not min_temp and not max_temp:
        pass
    else:
        filtered_df = filtered_df.loc[(filtered_df['Temp Nacelle (°C)'] >= min_temp) &
                                  (filtered_df['Temp Nacelle (°C)'] <= max_temp)]
    if not min_genspeed and not max_genspeed:
        pass
    else:
        filtered_df = filtered_df.loc[(filtered_df['Speed Generator (rpm)'] >= min_genspeed) &
                                  (filtered_df['Speed Generator (rpm)'] <= max_genspeed)]

    filtered_df.sort_values(by=['Time'], inplace=True, ascending=False)
    col_name = "Time"
    first_col = filtered_df.pop(col_name)
    filtered_df.insert(0, col_name, first_col)

    return filtered_df


def class_mode_selection(df, class_mode):
    class_mode = int(class_mode)
    if class_mode == 1:
        df = class_01(df)
    elif class_mode == 2:
        df = class_02(df)
    elif class_mode == 3:
        df = class_03(df)
    else:
        df = class_04(df)

    return df


def read_data(unit_num):
    """ This function has been build for reading HDF files and returns a pandas dataframe"""
    # input is the unit number which is an string variable and shows each WTG dataframe

    from pandas import read_hdf
    unit_num = 'Kahak/WTG ' + str(unit_num)
    df = read_hdf(unit_num)
    return df


def datetime_filter(df, start_date, end_date):
    """This function has been build for filtering data from a start time to an end time and returns a
    filtered dataframe"""

    # inputs: df: dataframe
    # start_date: considered variable for starting date - string type data
    # end_date: considered variable for end date - string type data

    filtered_dates = df[(df.Time >= start_date) & (df.Time <= end_date)]

    return filtered_dates


def class_01(df):
    df_class01 = df.loc[(df['PLU1 Pitch Angle PS1 (°)'] <= 0.5) & (df['PLU1 Pitch Angle PS1 (°)'] >= -0.5) &
                        (df['GridRealPower (kW)'] >= 2200) & (df['GridRealPower (kW)'] <= 2470)]

    df_class01.sort_values(by=['Time'], inplace=True, ascending=False)
    col_name = "Time"
    first_col = df_class01.pop(col_name)
    df_class01.insert(0, col_name, first_col)

    return df_class01


def class_02(df):
    df_class02 = df.loc[(df['PLU1 Pitch Angle PS1 (°)'] < 7) & (df['PLU1 Pitch Angle PS1 (°)'] > 0.5) &
                        (df['GridRealPower (kW)'] > 2470) & (df['GridRealPower (kW)'] <= 2600)]

    df_class02.sort_values(by=['Time'], inplace=True, ascending=False)
    col_name = "Time"
    first_col = df_class02.pop(col_name)
    df_class02.insert(0, col_name, first_col)

    return df_class02


def class_03(df):
    df_class03 = df.loc[(df['PLU1 Pitch Angle PS1 (°)'] <= 30) & (df['PLU1 Pitch Angle PS1 (°)'] >= 7) &
                        (df['GridRealPower (kW)'] > 2470) & (df['GridRealPower (kW)'] <= 2600)]

    df_class03.sort_values(by=['Time'], inplace=True, ascending=False)
    col_name = "Time"
    first_col = df_class03.pop(col_name)
    df_class03.insert(0, col_name, first_col)

    return df_class03


def class_04(df):
    df_class04 = df.loc[(df['PLU1 Pitch Angle PS1 (°)'] <= 0.5) & (df['PLU1 Pitch Angle PS1 (°)'] >= -0.5) &
                        (df['GridRealPower (kW)'] < 2200)]

    df_class04.sort_values(by=['Time'], inplace=True, ascending=False)
    col_name = "Time"
    first_col = df_class04.pop(col_name)
    df_class04.insert(0, col_name, first_col)

    return df_class04


def class_performance(df, time_duration, unit_num):
    import pandas
    unit_num = 'WTG ' + str(unit_num)
    import plotly.graph_objects as go

    if time_duration == 0:
        df = df.iloc[0:288, :]
        state = 'Last 24 hours'
        total_shape = df.shape[0]
        shape_class_01 = class_01(df).shape[0]
        shape_class_02 = class_02(df).shape[0]
        shape_class_03 = class_03(df).shape[0]
        shape_class_04 = class_04(df).shape[0]

        labels = ['Class 01: pitch angle=0, 2200<power<2470', 'Class 02: 0<pitch angle<7, 2470<power',
                  'Class 03: 7<pitch angle<30, power>2470', 'Class 04: power<2200']
        values = [shape_class_01, shape_class_02, shape_class_03, shape_class_04]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4)])

        fig.show()
    elif time_duration == 1:
        df = df.iloc[0:288 * 7, :]
        state = 'Last week'

        total_shape = df.shape[0]
        shape_class_01 = class_01(df).shape[0]
        shape_class_02 = class_02(df).shape[0]
        shape_class_03 = class_03(df).shape[0]
        shape_class_04 = class_04(df).shape[0]

        labels = ['Class 01: pitch angle=0, 2200<power<2470', 'Class 02: 0<pitch angle<7, 2470<power',
                  'Class 03: 7<pitch angle<30, power>2470', 'Class 04: power<2200']
        values = [shape_class_01, shape_class_02, shape_class_03, shape_class_04]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4)])
        fig.show()

    elif time_duration == 2:
        df = df.iloc[0:288 * 30, :]
        state = 'Last month'

        total_shape = df.shape[0]
        shape_class_01 = class_01(df).shape[0]
        shape_class_02 = class_02(df).shape[0]
        shape_class_03 = class_03(df).shape[0]
        shape_class_04 = class_04(df).shape[0]

        labels = ['Class 01: pitch angle=0, 2200<power<2470', 'Class 02: 0<pitch angle<7, 2470<power',
                  'Class 03: 7<pitch angle<30, power>2470', 'Class 04: power<2200']
        values = [shape_class_01, shape_class_02, shape_class_03, shape_class_04]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4)])
        fig.show()

    else:
        df = df.iloc[0:288 * 90, :]
        state = 'Last 3 months'

        total_shape = df.shape[0]
        shape_class_01 = class_01(df).shape[0]
        shape_class_02 = class_02(df).shape[0]
        shape_class_03 = class_03(df).shape[0]
        shape_class_04 = class_04(df).shape[0]

        labels = ['Class 01: pitch angle=0, 2200<power<2470', 'Class 02: 0<pitch angle<7, 2470<power',
                  'Class 03: 7<pitch angle<30, power>2470', 'Class 04: power<2200']
        values = [shape_class_01, shape_class_02, shape_class_03, shape_class_04]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4)])
        fig.show()

    return


def steady_condition_filter(df, points=3, tol=0.02):
    import pandas as pd
    diff_calc = pd.DataFrame();
    for x in range(1, points + 1):
        window = df['Speed Generator (rpm)'].diff(periods=x)
        diff_calc = pd.concat([diff_calc, window], axis=1).rename(columns={'Speed Generator (rpm)': 'diff' + str(x)})
    diff_calc = abs(diff_calc)
    length_check = pd.DataFrame();
    for x in range(1, points + 1):
        df1 = pd.DataFrame(diff_calc['diff' + str(x)])
        df2 = tol * pd.DataFrame(df['Speed Generator (rpm)']).rename(columns={'Speed Generator (rpm)': 'diff' + str(x)})
        df3 = df2.subtract(df1)
        length_check = pd.concat([length_check, df3], axis=1)
    processed_data = df.iloc[points:, :]
    length_check2 = length_check.iloc[points:, :]
    processed_data = processed_data[(length_check2 > 0).all(axis=1)]
    processed_data = processed_data.reset_index()
    return processed_data


def data_type(df, state):
    if state == '0':
        df = df
    else:
        df = steady_condition_filter(df)
    return df


def add_processed_signals(df):
    df['Delta Rotor RPM (rpm)'] = df['Rotor Rpm IGR (rpm)'] - df['Rotor Rpm SafeSys (rpm)']
    # Generator Sensors -----------------------------------------------
    # Sensor name: Gen Delta Temp Coil L12 (°C)
    df['Gen Delta Temp Coil L12 (°C)'] = df['Gen Temp Coil L1 (°C)'] - df['Gen Temp Coil L2 (°C)']

    # Sensor name: Gen Delta Temp Coil L23 (°C)
    df['Gen Delta Temp Coil L23 (°C)'] = df['Gen Temp Coil L2 (°C)'] - df['Gen Temp Coil L3 (°C)']

    # Sensor name: Gen Delta Temp Coil L13 (°C)
    df['Gen Delta Temp Coil L13 (°C)'] = df['Gen Temp Coil L1 (°C)'] - df['Gen Temp Coil L3 (°C)']

    # Sensor name: Gen Delta Temp Cooling Water (°C)
    df['Gen Delta Temp Cooling Water (°C)'] = df['Gen Temp CoolWaterFlow (°C)'] - df['Gen Temp CoolWaterReturn (°C)']

    # Gearbox Sensors -----------------------------------------------------
    # Sensor name: MGB Delta Temp Cooling (°C)
    df['MGB Delta Temp Cooling (°C)'] = df['MGB Temp CoolWaterFlow (°C)'] - df['MGB Temp CoolWaterReturn (°C)']

    # Converter Sensors ---------------------------------------------------
    # Sensor name: Inv Delta Temp Cooling (°C)
    df['Inv Delta Temp Cooling (°C)'] = df['Inv Temp Cooling Water Cold (°C)'] - df['Inv Temp Cooling Water Hot (°C)']
    return df


def processed_data(df):
    df = df.dropna(how='all')
    df.drop(df[(df['GridRealPower (kW)'] < 0)].index, inplace=True)
    df.drop(df[(df['GridRealPower (kW)'] > 0) & (df['Wind Speed #1 (m/s)'] < 1)].index,
            inplace=True)
    df.drop(df[(df['PLU1 Pitch Angle PS1 (°)'] < 0.5) & (df['Wind Speed #1 (m/s)'] > 12)].index,
            inplace=True)

    return df
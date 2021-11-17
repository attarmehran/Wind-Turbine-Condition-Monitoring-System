def wind_data_builder():
    from pandas import read_excel
    from pandas import concat
    from pandas import to_datetime
    from pandas import read_pickle
    from pandas import DataFrame
    from turbineView.Database_Tools import read_data

    unit_num = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
                '18', '19', '20', '21', '22']
    df = DataFrame()

    for i in unit_num:
        data = read_data(i)
        wind_speed = data['Wind Speed #1 (m/s)']
        wind_speed = DataFrame(wind_speed)
        wind_speed.reset_index(inplace=True, drop=True)
        df = concat([df, wind_speed], axis=1)
    df.to_pickle('Wind_Data')

    return


def real_power_data_builder():
    from pandas import read_excel
    from pandas import concat
    from pandas import to_datetime
    from pandas import read_hdf
    from pandas import DataFrame
    from turbineView.Database_Tools import read_data

    unit_num = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
                '18', '19', '20', '21', '22']
    df = DataFrame()

    for i in unit_num:
        data = read_data(i)
        power = data['GridRealPower (kW)']
        power = DataFrame(power)
        power.reset_index(inplace=True, drop=True)
        df = concat([df, power], axis=1)
    df.to_pickle('Power_Data')

    return


def grid_frequencey_builder():
    from pandas import read_excel
    from pandas import concat
    from pandas import to_datetime
    from pandas import read_hdf
    from pandas import DataFrame
    from turbineView.Database_Tools import read_data

    unit_num = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
                '18', '19', '20', '21', '22']
    df = DataFrame()

    for i in unit_num:
        data = read_data(i)
        fr = data['GridFrequency (Hz)']
        fr = DataFrame(fr)
        fr.reset_index(inplace=True, drop=True)
        df = concat([df, fr], axis=1)
    df.to_pickle('Frequency_Data')

    return



def live_data_cards(farm_name):
    from pandas import read_pickle
    from numpy import mean

    wind_ave = 0
    df = read_pickle("./{}/Wind_Data".format(farm_name))
    df = df.fillna(0)
    for i in range(22):
        wind_ave += df.iloc[0, i]
    wind_ave = wind_ave / 22

    freq_ave = 0
    df = read_pickle("./{}/Frequency_Data".format(farm_name))
    df = df.fillna(50)
    for i in range(22):
        freq_ave += df.iloc[0, i]

    freq_ave = freq_ave / 22

    power_ave = 0
    df = read_pickle("./{}/Power_Data".format(farm_name))
    df = df.fillna(0)
    for i in range(22):
        power_ave += df.iloc[0, i]

    temp_ave = 0
    df = read_pickle("./{}/OutdoorTemp_Data".format(farm_name))
    df = df.fillna(0)
    for i in range(22):
        temp_ave += df.iloc[0, i]

    temp_ave = temp_ave / 22

    return round(wind_ave, 2), f"{round(power_ave):,}", round(freq_ave, 2), round(temp_ave)

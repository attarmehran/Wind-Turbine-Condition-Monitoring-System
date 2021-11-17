

def read_data(unit_num):
    """ This function has been built for reading HDF files and returns a pandas dataframe"""
    # input is the unit number which is an string variable and shows each WTG dataframe

    from pandas import read_hdf
    unit_num = './Kahak/WTG ' + str(unit_num)
    df = read_hdf(unit_num)

    return df

def datetime_filter(df,start_date,end_date):
    """This function has been build for filtering data from a start time to an end time and returns a
    filtered dataframe"""

    # inputs: df: dataframe
    # start_date: considered variable for starting date - string type data
    # end_date: considered variable for end date - string type data

    filtered_dates = df[(df.Time>=start_date)&(df.Time<=end_date)]

    return filtered_dates

def databasebuilder(unit_num,new_file):
    """This function has been build for updating the database and returns a the updated dataframe as
    a HDF file format"""

    # inputs:
    # unit_num: a variable which shows the unit number WTG # - string data type
    # new_file: a csv file which the user wants to add to the database - csv file

    from pandas import read_excel
    from pandas import concat
    from pandas import to_datetime
    from pandas import read_hdf
    from pandas import DataFrame

    unit_num = 'WTG ' + str(unit_num)

    try:
        df = read_hdf(unit_num)
    except:
        df = DataFrame()
        df.to_hdf(unit_num, key = unit_num)
        df = read_hdf(unit_num)

    df_new = read_excel(new_file)

    df = concat([df_new,df]).drop_duplicates()
    to_datetime(df.Time)
    df.sort_values(by=['Time'], inplace=True, ascending=False)
    col_name="Time"
    first_col = df.pop(col_name)
    df.insert(0, col_name, first_col)
    df.reset_index(inplace=True,drop=True)
    Time = df['Time']
    Last_Time_Updated = Time.iloc[0]
    df.to_hdf(unit_num, key = unit_num, complevel = 5, mode = 'w')
    status = str(unit_num) + ' Successfully Updated !' + ',' + ' Last Time Updated = ' + str(Last_Time_Updated)
    return status

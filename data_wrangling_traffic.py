import os 
import pandas as pd
import numpy as np



##################------------NEW GENERATE BIG DF-------------------#################
def wrangle_it():
    print('Wrangling traffic data')
    input_data_df_list = []
    pollutant_name = []

    directory = r'data/traffic_input_data'
    input_files = os.listdir(directory)
    #sep = ' 1 Hours Avg.csv' #Set separation for file_names

    for file_name in input_files:
      #  station_name = file_name.split(sep, 1)[0]
        file_dir = directory + '/' + file_name
        df = pd.read_excel(file_dir)
     #   df = df.assign(Station = station_name)
        input_data_df_list.append(df)

    # Creates a huge df with all data
    data = pd.concat(input_data_df_list)
    # Adds the month column
    data['To Date'] = pd.to_datetime(data['STAD'])

    data["Month"] = pd.DatetimeIndex(data["To Date"]).month_name()
    data["Month Index"] = pd.DatetimeIndex(data["To Date"]).month
    data["Day"] = pd.DatetimeIndex(data["To Date"]).day_name()
    data["Day Index"] = pd.DatetimeIndex(data["To Date"]).dayofweek
    data['Day of Month'] = pd.DatetimeIndex(data['To Date']).day
    data["Hour"] = pd.DatetimeIndex(data["To Date"]).hour
    data["Date"] = pd.DatetimeIndex(data["To Date"]).date
    data["Year"] = pd.DatetimeIndex(data["To Date"]).year
    #data = data[['STAD', 'Runway']]
    data['Runway'] = data['Runway'].str.replace('-','')
    data['Runway'] = data['Runway'].str.replace('A','')
    data['Runway'] = data['Runway'].str.replace('D','')
    data=data.sort_values('To Date', ascending=False)
    #data = data.dropna()
    #data = data.drop(['Call Sign', 'Passenger Handling Agent', 'Ramp Handling Agent', 'Cargo Handling Agent', 'Maintenance Handling Agent'], axis='columns')

    data = data[['To Date', 'Month', 'Month Index', 'Day', 'Day Index', 'Year',
                 'Day of Month', 'Hour', 'Date', 'Runway', 'Air Terminal']]



    data.to_csv('data/traffic.csv', index=False)
    pass

import pandas as pd 
import os 
import numpy as np

#------------------SCRIPT FOR DATA WRANGLING ONLY RUN ONCE---------------###


def wrangle_it():
    print('Wrangling pollutant data')
    timespans = ['1', '8', '24']

    for h in timespans:
        input_data_df_list = []
     
      
        #directory = r'data/24h'
        directory = r'data/'+h+'h'
        input_files = os.listdir(directory)
        #sep = ' 24 Hours Avg.csv' #Set separation for file_names
        sep = ' '+h+' Hours Avg.csv' #Set separation for file_names
        
        for file_name in input_files:
            station_name = file_name.split(sep, 1)[0]
            file_dir = directory + '/' + file_name
            df = pd.read_csv(file_dir)
            df = df.assign(Station = station_name)
            input_data_df_list.append(df)
        
        # Creates a huge df with all data
        data = pd.concat(input_data_df_list).fillna(0)
        # Adds the month column
        data["Month"] = pd.DatetimeIndex(data["To Date"], dayfirst=True).month_name()
        data["Month Index"] = pd.DatetimeIndex(data["To Date"], dayfirst=True).month
        data["Day"] = pd.DatetimeIndex(data["To Date"], dayfirst=True).day_name()
        data["Day Index"] = pd.DatetimeIndex(data["To Date"], dayfirst=True).dayofweek
        data["Hour"] = pd.DatetimeIndex(data["To Date"], dayfirst=True).hour
        data["Year"] = pd.DatetimeIndex(data["To Date"], dayfirst=True).year
        data["Date"] = pd.DatetimeIndex(data["To Date"], dayfirst=True).date
        
        # Data wrangling for windrose
        data['Wind Speed (m/s)'] = pd.to_numeric(data['Wind Speed (m/s)'], errors='coerce')
        data['Wind Direction (degree)'] = pd.to_numeric(data['Wind Direction (degree)'], errors='coerce')
        data['Wind Speed (km/h)'] = data['Wind Speed (m/s)']*3.6
        #data['Wind Speed (km/h)'] = data[data['Wind Speed (km/h']>0]['Wind Speed (km/h)']
        
        directions = np.array(['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW',
                               'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW', 'N'])
        data['To Date'] = pd.to_datetime(data['To Date'], dayfirst=True)
        data=data.sort_values(by='To Date').reset_index(drop=True)
        data=data.dropna()
        data=data.replace('-', np.nan)
        data['Wind Direction (compass)'] = data['Wind Direction (degree)'].apply(
                lambda x: directions[round(x/22.5)])
        
        data.to_csv('data/'+h+"h.csv", index=False)
        pass

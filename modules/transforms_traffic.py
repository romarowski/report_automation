import os
import pandas as pd
import numpy as np


#traffic_df = pd.read_excel(r"data/traffic_input_data/AODB_MAY_2020.xlsx") 
#
#pctge_flights_per_terminal = traffic_df['Air Terminal'].value_counts(normalize=True) * 100
#
##Prepare dataset for weekly trend
#
#flights_by_date = pd.DataFrame(traffic_df['ETAD'])
#flights_by_date['To Date'] = pd.to_datetime(flights_by_date['ETAD'])
#count_weekly_flights = flights_by_date.groupby(flights_by_date['To Date'].dt.isocalendar().week).count()
#count_weekly_flights = np.array(count_weekly_flights['To Date'])
#
#
#button_format = get_weekly_flight_trend.button_format(count_weekly_flights)

data = pd.read_csv('data/traffic.csv')
data['Date'] = pd.to_datetime(data['Date'])


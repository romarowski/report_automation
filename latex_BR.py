import numpy as np
import pandas as pd
from modules import coordinates, transforms_pollutants, transforms_traffic
from modules import latex
from modules.latex import check_stations_data, sensor_numbers, wind, noise,\
                          traffic, dates, terminal, runway, poll_month,\
                          poll_limits, poll_temporal, poll_max, aqi, \
                          convert_limits, conc_limits
import pdb
import os

def make_latex(start_date, end_date): 
    print('Generating latex')
    oneHourPoll = transforms_pollutants.data
    eightHourPoll = transforms_pollutants.data8
    twofourHourPoll = transforms_pollutants.data24
    trafficDF = transforms_traffic.data
    limitsDF = transforms_pollutants.limits
    coords_df = coordinates.coords_df
    #pdb.set_trace()
    sites = sorted(oneHourPoll['Station'].unique(), key=str.casefold)

    poll = ['CO (mg/m³)', 'NO₂ (µg/m³ )', 'O₃ (µg/m³ )',
            'H₂S (µg/m³ )', 'NO (µg/m³ )', 'SO₂ (µg/m³)','PM₂.₅ (µg/m³ )',
            'PM₁₀ (µg/m³)','Leq (dB)']

    #Pick dates
    #start_date = '2021-03-01'
    #end_date = '2021-03-31'

    if os.path.exists("mystyle.sty"):
      os.remove("mystyle.sty")
    f = open("mystyle.sty", "a")
    f.write('\ProvidesPackage{mystyle}\n')

    dates_text = dates.info(start_date, end_date)
    f.write(dates_text)

    empty_stations = check_stations_data.check(start_date, end_date,
            sites, oneHourPoll)
    f.write(empty_stations)
    nbr_station = sensor_numbers.number(sites)
    f.write(nbr_station)
    wind_text = wind.stats('Privet Aviation', start_date, end_date, 
            twofourHourPoll)
    f.write(wind_text)
    noise_text = noise.stats(start_date,end_date, oneHourPoll, var='Leq (dB)')
    f.write(noise_text)
    traffic_text = traffic.stats_by_time(start_date, end_date, trafficDF)
    #pdb.set_trace()
    f.write(traffic_text)

    terminal_text = terminal.info(start_date, end_date, trafficDF)
    f.write(terminal_text)

    runway_text = runway.info(start_date, end_date, trafficDF)
    f.write(runway_text)

    exceeders = []

    for pollutant in poll:
        poll_text = poll_month.info(oneHourPoll, start_date, pollutant)
        f.write(poll_text)
        #pdb.set_trace()
        if pollutant in limitsDF['Pollutant'].to_numpy():      
            time = limitsDF[limitsDF['Pollutant']==pollutant].\
                    iloc[0]['Averaging time [h]']
            if time == 1:
                poll_df = oneHourPoll
            elif time == 8:
                poll_df = eightHourPoll
            else:
                poll_df = twofourHourPoll
            lim_text, exceeds = poll_limits.info(pollutant, poll_df, limitsDF, 
                    start_date, end_date)
            f.write(lim_text)
            if exceeds:
                exceeders += [pollutant]
        poll_text = poll_temporal.info(pollutant, start_date, end_date, oneHourPoll)
        f.write(poll_text)
        poll_text = poll_max.info(pollutant, start_date, end_date, oneHourPoll, 
                trafficDF)
        f.write(poll_text)

    conc_text = conc_limits.info(exceeders)
    f.write(conc_text)
    AQI_text = aqi.stats(start_date, end_date, oneHourPoll)
    f.write(AQI_text)
    conversions_text = convert_limits.info(start_date, end_date, oneHourPoll)
    f.write(conversions_text)

    f.write('\endinput')
    f.close()
    pass

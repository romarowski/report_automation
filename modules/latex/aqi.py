from modules.latex import filter_dates 
import pdb
def stats(start_date, end_date, poll_df):
    var = ' USAQI'
    poll_df = filter_dates.filtered(start_date, end_date, poll_df)
    #pdb.set_trace()
    df_mean = poll_df.groupby(by='Station', as_index=False)[var].mean()
    df_mean = df_mean[[var, 'Station']].reset_index(drop=True)
    max_station = df_mean[df_mean[var]==df_mean[var].max()].\
            iloc[0]['Station']
    text = '\\newcommand{\maxStationAQI}{'+max_station+'}\n'
    if df_mean[var].max() <= 50:
        text += '\\newcommand{\\analysisAQI}{All average values obtained for '+\
                'the stations during the analysed period were below 50, '+\
                'therefore they are categorised as “Good”, following the '+\
                'USEPA classification.}\n'
        text += '\\newcommand{\concAQI}{The average AQIs obtained fell into '+\
                'the category "Good" for all the stations}\n'
    else: 
        stations = df_mean[df_mean[var]>50]['Station']
        stations_text =''
        for station in stations:
            stations_text += station+'; '    
        text += '\\newcommand{\\analysisAQI}{'+stations_text+ ' had '+\
                'an average AQI for the studied period exceeding the '+\
                'USEPA "Good" rating.}\n'
        text += '\\newcommand{\concAQI}{Some stations exceeded the USEPA ' +\
                '"Good" rating}\n'

    return text       


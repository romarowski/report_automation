from modules.plotting import find_pollutant_max
from datetime import datetime
from modules.latex import replace_formula, winds_daily
import pdb
def info(pollutant, start_date, end_date, poll_df, traffic_df):
    #pdb.set_trace()
    site, date = find_pollutant_max(pollutant, start_date, end_date, poll_df)
    poll_name = replace_formula.replace(pollutant)
    text=winds_daily.stats(site, start_date, end_date, date, poll_df, poll_name)
    traffic_df = traffic_df[traffic_df['Date'] == date]
    poll_df = poll_df[(poll_df['Date']==date)&(poll_df['Station']==site)]
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    date_text = date_obj.strftime('%A, %d %B')
    poll_df = poll_df[[pollutant, 'Hour']].reset_index(drop=True)
    traffic_df = traffic_df.groupby('Hour', as_index=False)['To Date']\
            .count().reset_index(drop=True)
    traffic_df = traffic_df.rename(columns={'To Date':'Count'})
    correlation = poll_df[pollutant].corr(traffic_df['Count'])
    
    text += '\\newcommand{\dayMax'+poll_name+'}{'+date_text+'}\n'
    text += '\\newcommand{\stationMax'+poll_name+'}{'+site+'}\n'
    max_hour_tr = traffic_df[traffic_df['Count']==traffic_df['Count'].max()].\
            iloc[0]['Hour']
    max_hour_po = poll_df[poll_df[pollutant]==poll_df[pollutant].max()].\
            iloc[0]['Hour']
    if max_hour_tr == max_hour_po:
        text += '\\newcommand{\\relTrafficMax'+poll_name+'}{coincides with a'+\
                ' maximum in traffic indicating a possible correlation '+\
                'between measurement levels and traffic}\n'
    else:
        text += '\\newcommand{\\relTrafficMax'+poll_name+'}{does not ' +\
                'coincide with a maximum in traffic indicating a loose '+\
                'correlation between measurement levels and traffic}\n'

    text += '\\newcommand{\correl'+poll_name+'}{'+f'{correlation:.2f}'
    if abs(correlation) < .1:
        text += ' indicating null correlation'
    elif (abs(correlation) >= .1 and abs(correlation) < .3):
        text += ' indicating small correlation'
    elif (abs(correlation) >= .3 and abs(correlation) < .5):
        text += ' indicating medium correlation'
    else:
        text += ' indicating large correlation'
    text += '}\n'
    return text

from rosely import WindRose
from modules.latex import winds_monthly
import pdb
def stats(site, start_date, end_date, date, poll_df, poll_name):   
    #pdb.set_trace()
    wr_month = winds_monthly.info(site, start_date, end_date, poll_df)
    poll_df = poll_df[(poll_df['Date']==date) & (poll_df['Station']==site)]
    #wind_df = poll_df.groupby('Wind Direction (compass)', as_index=False)\
    #        ['Wind Speed (km/h)'].mean()
    
    wind_df = poll_df[['Wind Speed (km/h)', 'Wind Direction (compass)']]
    max_day = wind_df[wind_df['Wind Speed (km/h)'].max()==\
            wind_df['Wind Speed (km/h)']]
    max_dir = max_day.iloc[0]['Wind Direction (compass)']
    max_speed_avg = max_day.iloc[0]['Wind Speed (km/h)']
    max_month_qt = wr_month[wr_month['Wind Direction (compass)']==max_dir].\
            iloc[0]['Wind Speed (km/h)']
    

    if max_month_qt < max_speed_avg:
        text = '\\newcommand{\wind'+poll_name+'}{wind was blowing with a high'+\
               ' strength from the '+ max_dir+'. Indicating a link between '+\
               'external sources and pollutant levels.}\n'
    else:
        text = '\\newcommand{\wind'+poll_name+'}{wind was mostly blowing with'+\
               ' no particuarly high speeds. Indicating a weak correlation '+\
               'between external sources and pollutant levels.}\n'
    return text


# Old Procedure
#    wr_df = poll_df[['Wind Speed (km/h)',  'Wind Direction (degree)']]
#    names = { 'Wind Speed (km/h)': 'ws',  'Wind Direction (degree)':'wd'}
#    wr_df[wr_df['Wind Speed (km/h)']<0] = 0
#    WR = WindRose(wr_df)
#    WR.calc_stats(normed=True, bins=6, variable_names=names)
#    wind_df = WR.wind_df
#    max_speed = wind_df['speed'].max()
#    max_dir = wind_df[wind_df['speed']==max_speed].iloc[0]['direction']
#    max_speed_avg = .5*(float(max_speed.split('-')[0])+\
#                        float(max_speed.split('-')[1]))
#    max_month = wr_month[wr_month['direction']==max_dir]['speed'].max()
#    max_month_avg =  .5*(float(max_month.split('-')[0])+\
#                         float(max_month.split('-')[1]))

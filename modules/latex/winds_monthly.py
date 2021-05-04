#from rosely import WindRose
from modules.latex import filter_dates
def info(site, start_date, end_date, poll_df):
    poll_df = filter_dates.filtered(start_date, end_date, poll_df)
    poll_df = poll_df[poll_df['Station']==site]
    wind_df = poll_df.groupby('Wind Direction (compass)', as_index=False)\
            ['Wind Speed (km/h)'].quantile(q=.75)
    return wind_df

# Old procedure
#    wr_df = poll_df[['Wind Speed (km/h)',  'Wind Direction (degree)']]
#    names = { 'Wind Speed (km/h)': 'ws',  'Wind Direction (degree)':'wd'}
#    wr_df[wr_df['Wind Speed (km/h)']<0] = 0
#    WR = WindRose(wr_df)
#    WR.calc_stats(normed=True, bins=6, variable_names=names)

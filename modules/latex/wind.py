from rosely import WindRose
import pdb
def stats(site, start_date, end_date, poll_df):
    #Returns 2 most frequent wind directions and max wind speed.
    poll_df = poll_df[(poll_df['Date']>=start_date) &\
            (poll_df['Date']<=end_date) & (poll_df['Station']==site)]
    wr_df = poll_df[['Wind Speed (km/h)',  'Wind Direction (degree)']]
    names = { 'Wind Speed (km/h)': 'ws',  'Wind Direction (degree)':'wd'}
    wr_df[wr_df['Wind Speed (km/h)']<0] = 0
    WR = WindRose(wr_df)
    WR.calc_stats(normed=True, bins=6, variable_names=names)
    WR.wind_df = WR.wind_df.sort_values(by='speed')
    max_speed = WR.wind_df['direction'].iloc[-1]
    WR.wind_df = WR.wind_df.sort_values(by='frequency')
    max_freq = WR.wind_df['direction'].iloc[-2:].to_numpy()
    freq_text = '\\newcommand{\\freqWinds}{'+max_freq[0]+' and '+max_freq[1]+'}'
    max_text = '\\newcommand{\maxWind}{'+max_speed+'}'
    text = freq_text + "\n" + max_text + "\n"
    
    return text

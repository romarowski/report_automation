import pdb
from modules.latex import filter_dates
def info(start_date, end_date, traffic_df):
    df = filter_dates.filtered(start_date, end_date, traffic_df) 
    df_count = df.groupby('Runway')['To Date'].count().reset_index()
    pdb.set_trace()
   
    max_runways=df_count.sort_values(by='To Date').reset_index(drop=True)\
            ['Runway'].iloc[-2:].to_numpy()

    text = '\\newcommand{\maxRunway}{'+max_runways[1]+\
            ', followed by Runway '+max_runways[0]+'}\n'
    return text

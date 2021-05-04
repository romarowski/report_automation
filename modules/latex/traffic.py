import pdb
import pandas as pd
def stats_by_time(start_date, end_date, traff_df):
    #Returns info on traffic statistics. MAYBE BREAK THIS FUNCTION UP 
    text=''
    df = traff_df
    df_filter = df[(df['To Date']>=start_date) & (df['To Date']<=end_date)]
    for query in ['Hour', 'Month', 'Day']:
        if query == 'Month':
            df_count = df.groupby(query, as_index=False)['To Date'].count()
            change = df_count['To Date'].pct_change().iloc[-1]
            if change < 0:
                change_text = 'decrease'
            else:
                change_text = 'increase'
            change = abs(round(change,3))*100
            text += '\\newcommand{\\trafficChange}{'+str(change)+'\% '+\
                    change_text+'}\n'
           # pdb.set_trace()
        elif query == 'Hour':
            df_count = df_filter.groupby(query, as_index=False)['To Date'].\
                    count()
            b = [0,4,8,12,16,20,24]
            l = ['Late at Night', 'during the Early Morning',
                    'in the Morning', 'at Noon','during the Evening','at Night']
            df_count['Period'] = pd.cut(df_count['Hour'], bins=b, 
                    labels=l, include_lowest=True)
            df_mean = df_count.groupby('Period', as_index=False)['To Date'].\
                    mean()
           #pdb.set_trace()
            max_period = df_mean[df_mean['To Date'] == df_mean['To Date']\
                    .max()]['Period'].reset_index(drop=True)[0]
            text += '\\newcommand{\\trafficPeriod}{'+max_period+'}\n'
            max_query = df_count[df_count['To Date'] == df_count['To Date']\
                    .max()][query].reset_index(drop=True)[0]
            text += '\\newcommand{\\traffic'+query+'}{'+str(max_query)+'h}\n'
        elif query == 'Day':
            df_count = df_filter.groupby(query, as_index=False)['To Date'].\
                    count()
            max_query = df_count[df_count['To Date'] == df_count['To Date']\
                    .max()][query].reset_index(drop=True)[0]
            text += '\\newcommand{\\traffic'+query+'}{'+str(max_query)+'s}\n'
    return text

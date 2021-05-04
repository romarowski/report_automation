from modules.latex import filter_dates
def stats(start_date, end_date, poll_df, var):
    poll_df = filter_dates.filtered(start_date, end_date, poll_df)
    
    poll_df = poll_df.groupby('Station', as_index=False).mean().reset_index()
    
    maxi = poll_df[poll_df[var] == poll_df[var].max()]['Station'].\
            reset_index(drop=True)[0]
    mini = poll_df[poll_df[var] == poll_df[var].min()]['Station'].\
            reset_index(drop=True)[0]
    maxi_value = poll_df[var].max()
    text = '\\newcommand{\maxNoise}{'+maxi+'}'+'\n'+'\\newcommand{\minNoise}{'+\
            mini+'}\n'
    text += '\\newcommand{\maxNoiseValue}{'+f'{maxi_value:.2f}'+'}\n'
    return text



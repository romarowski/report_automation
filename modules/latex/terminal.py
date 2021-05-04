import pdb
from modules.latex import filter_dates
def info(start_date, end_date, traffic_df):
    df = filter_dates.filtered(start_date, end_date, traffic_df) 
    df_count = df.groupby('Air Terminal')['To Date'].count().reset_index()
    max_terminal = df_count[df_count['To Date'] == df_count['To Date']\
            .max()]['Air Terminal'].reset_index(drop=True)[0]
    text = '\\newcommand{\maxTerminal}{'+max_terminal+'}\n'
    return text

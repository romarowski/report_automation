from modules.latex.filter_dates import filtered
from modules.latex.timeday_cut import cutted
from modules.latex import replace_formula
import pdb
def info(poll, start_date, end_date, poll_df):
    poll_df = filtered(start_date, end_date, poll_df)
    df_cut = cutted(poll_df)
    df_mean = df_cut.groupby(by='Period', as_index=False)[poll].mean()
    max_period = df_mean[df_mean[poll]==df_mean[poll].max()].iloc[0]['Period']
    min_period = df_mean[df_mean[poll]==df_mean[poll].min()].iloc[0]['Period']
    poll_name = replace_formula.replace(poll)
    text = '\\newcommand{\minDaily'+poll_name+'}{'+min_period+'}\n'
    text += '\\newcommand{\maxDaily'+poll_name+'}{'+max_period+'}\n'
    return text


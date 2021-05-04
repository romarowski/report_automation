import pdb 
from modules.latex import replace_formula
from modules.latex.filter_dates import filtered
def info(poll, poll_df, limits_df, start_date, end_date):
    #pdb.set_trace()
    exceed = False
    poll_df = filtered(start_date, end_date, poll_df)
    df = poll_df[poll_df[poll]>\
            limits_df[limits_df['Pollutant']==poll].iloc[0]['Level']]
    df = df.reset_index(drop=True)
    poll_name = replace_formula.replace(poll)
    if not df.empty:
        count = len(df.index)
        text = '\\newcommand{\\treshold'+poll_name+'}{surpass ' #+\
               # str(count)+ ' time'
        #if count >1:
        #    text+= 's'
        text += '}\n'
        exceed = True
        #days = df['To Date']
        #for day in days:
        #    text += 
    else:
        text = '\\newcommand{\\treshold'+poll_name+'}{be below}\n'
    
    return text, exceed


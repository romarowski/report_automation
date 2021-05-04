from datetime import datetime
import pdb
from modules.latex import replace_formula
def info(poll_df, start_date, poll):
    
    dt = datetime.strptime(start_date, '%Y-%m-%d')
    #This line depends on the available data!
    #df = poll_df[poll_df['Year']==dt.year][[poll, 'Month']]
    df = poll_df[[poll, 'Month']]
    df = df.groupby(by='Month')[poll].mean().reset_index(name="Avg")
    #pdb.set_trace()
    change = df['Avg'].pct_change().iloc[-1]

    if change < 0:
        change_text = 'decrease'
    else:
        change_text = 'increase'
    change = abs(change)*100
    change_text = '{:.1f}'.format(change) +'\% '+ change_text
    poll_name = replace_formula.replace(poll)
    
    text = '\\newcommand{\monthChange'+poll_name+'}{'+change_text+' }\n'
    return text

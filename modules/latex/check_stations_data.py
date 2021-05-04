from modules.latex import filter_dates
import numpy as np
def check(start_date, end_date, sites, df):
    #Checks which sites have data and returns string for printing.

    df = filter_dates.filtered(start_date, end_date, df)
    #df[(df['To Date'] >= start_date) & (df['To Date'] <= end_date)]
    text = '\\newcommand{\emptystations}{' 
    for i, site in enumerate(sites):
        if  df[df['Station']==site].empty:
            if i==0:
                text += 'Note: The measurements corresponding to the' +\
                'following stations were not available for this' +\
                'study period:'
            text += site + ' ; '
    text += '}\n'
    text += '\\newcommand{\\fullstations}{'+str(np.size(sites))+'}\n' 
    return text

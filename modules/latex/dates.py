from datetime import datetime, date
def info(start_date, end_date):
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d')
    today = date.today()
    #Add here some check that is monthly report
    text = '' 
    text += '\\newcommand{\monthyear}{'+start_dt.strftime("%B")+\
            ' '+str(start_dt.year)+'}\n'
    text += '\\newcommand{\onlymonth}{'+start_dt.strftime("%B")+'}\n'
    text += '\\newcommand{\\reportfootname}{RUH LAQ and Noise Monthly ' +\
            'Report, '+start_dt.strftime("%B") +' '+str(start_dt.year)+'}\n'
    text += '\\newcommand{\datedon}{'+today.strftime("%B")+' '+\
    str(today.year)+'}\n'
    return text

def filtered(start_date, end_date, df):
    df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)].\
            reset_index(drop=True)
    return df

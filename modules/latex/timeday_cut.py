import pandas as pd
def cutted(df):
     b = [0,4,8,12,16,20,24]
     l = ['Late at Night', 'during the Early Morning',
          'in the Morning', 'during the Afternoon','during the Evening',
          'at Night']
     df['Period'] = pd.cut(df['Hour'], bins=b,
         labels=l, include_lowest=True)
     return df
 

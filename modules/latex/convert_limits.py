from modules.latex import filter_dates
def info(start_date, end_date, poll_df):
    poll_df = filter_dates.filtered(start_date, end_date, poll_df)
    T_avg = poll_df['Temperature (°C)'].mean() 
    T_avg += 273.15 #Kelvin
    molar_mass= {'CO': 28.01, #g/mol
                'Othree': 48,
                'NOtwo':  46,
                'SOtwo': 64.07,
                }
    p = 101325 #Pa
    R = 8.3145 #m^3 Pa K^-1 mol^-1
    limit = {'CO': 35, #ppm
             'Othree': .07, #ppm
             'NOtwo': 100, #ppb
             'SOtwo': 75, #ppb
             }
    text = ''
    for pollutant in molar_mass:
        limit_density = limit[pollutant]*molar_mass[pollutant]*p / \
                                  (R *  T_avg * 1e6)
        if pollutant == 'Othree':
            limit_density *= 1e3
        limit_density *= 1e3
        text +='\\newcommand{\limit'+pollutant+'}{'+f'{limit_density:.0f}'+'}\n'
    
    return text


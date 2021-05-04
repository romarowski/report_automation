import plotly.express as px
import pandas as pd 
import plotly.graph_objs as go
import plotly.figure_factory as ff
import numpy as np
import pdb, traceback, sys, code
import datetime
import scipy.stats

from pandas.api.types import CategoricalDtype
from plotly.subplots import make_subplots
from plotly.validators.scatter.marker import SymbolValidator
from datetime import date 
from rosely import WindRose

def location_map(lat_lon_df, station):
   #Highlights a station 
    coords_df = lat_lon_df

    coords_df = coords_df.sort_values(by='Station')
    coords_df['Location'] = coords_df['Station'] == station


    #Generate figure       
    fig = px.scatter_mapbox(coords_df, lat="lat", lon="lon", 
             color='Location',
             hover_name="Station", zoom=12, height=400, 
             color_discrete_sequence=['green', 'red']) 
    fig.update_layout(mapbox_style="open-street-map")  
    #fig.update_layout(title_text='Air Quality Index for: ' + months[-1],
    #                  title_x=0.1, title_y=.97)
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
    fig.update_traces(marker=dict(size=12))
    fig.data[0].update(hovertemplate = '<b>%{hovertext}</b><br><extra></extra>')

    fig.data[1].update(hovertemplate = '<b>%{hovertext}</b><br><extra></extra>')
    #pdb.set_trace()
    return fig


def AQI_map(lat_lon_df, pollutants_df):
        # Generates the AQI by station figure shown upon start-up. 
        # INPUT -> two pd.dataframes: 
        # 'lat_lon_df' -> gives latitude and longitude of each station.
        # 'pollutants_df' -> gives sensor measurements @ different stations.
        # OUTPUT -> one figure, px.scatter:
        # fig -> is a plotly fig of the type "open-street-map", with the mean AQI for the latest month available on the dataset 'pollutants_df' by station.

        coords_df = lat_lon_df
        poll_df = pollutants_df

        coords_df = coords_df.sort_values(by='Station')
        months_index = poll_df['Month Index'].unique()

        #Get latest month available
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
               'September', 'October', 'November', 'December']
        months = months[0:max(months_index)]

        poll_df = poll_df[poll_df['Month']==months[-1]].groupby('Station').mean()
        coords_df['AQI'] = poll_df[' USAQI'].round(1)
        coords_df.fillna(0)


        #Generate figure       
        fig = px.scatter_mapbox(coords_df, lat="lat", lon="lon", color='AQI',
             hover_name="Station", hover_data=['AQI'],
             color_continuous_scale=["blue", "green", "red"],
             zoom=12, height=400) 
        fig.update_layout(mapbox_style="open-street-map")  
        fig.update_layout(title_text='Air Quality Index for: ' + months[-1],
                          title_x=0.1, title_y=.97)
        fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig.update_traces(marker=dict(size=12))
        fig.data[0].update(hovertemplate = '<b>%{hovertext}</b><br><br>AQI=%{marker.color}<extra></extra>')

        #pdb.set_trace()
        return fig

def plot_wind_speed_direction(date_value, hour, site, df_p):
        #Gives a plot of wind speed and direction

        poll_df = df_p[(df_p['Date']==date_value)&(df_p["Station"]==site)&(df_p["Hour"]==hour)]
        #pdb.set_trace()
        u = poll_df['Wind Speed (km/h)'].to_numpy() * np.cos(3*np.pi/2-np.pi/180*poll_df['Wind Direction (degree)'].to_numpy())
        v = poll_df['Wind Speed (km/h)'].to_numpy() * np.sin(3*np.pi/2-np.pi/180*poll_df['Wind Direction (degree)'].to_numpy())

        poll_df_day = df_p[(df_p['Date']==date_value)&(df_p['Station']==site)].sort_values(by='Hour').reset_index(drop=True)

        maxu = poll_df_day['Wind Speed (km/h)'].to_numpy()*np.cos(np.pi/2-np.pi/180*poll_df_day['Wind Direction (degree)'].to_numpy())

        maxv = poll_df_day['Wind Speed (km/h)'].to_numpy()*np.sin(np.pi/2-np.pi/180*poll_df_day['Wind Direction (degree)'].to_numpy())

        maxu=np.max(np.abs(maxu))
        maxv=np.max(np.abs(maxv))
        fig = ff.create_quiver([0],[0],u,v, scale=1)#, scaleratio=0.5)
        fig.update_xaxes(range=[-maxu, maxu])
        fig.update_layout(plot_bgcolor='white')
        fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=False)
        fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=False)
        fig.update_yaxes(range=[-maxv, maxv])
        direction = invert_direction(str(poll_df['Wind Direction (compass)'].to_numpy()[0]))
        fig.update_layout(title='Wind Speed ' + str(poll_df['Wind Speed (km/h)'].to_numpy()[0]) + 'km/h towards ' + direction)
        return fig

def invert_direction(compass_in):
        if compass_in == 'N':
            compass_out = 'S'
        elif compass_in == 'NNE':
            compass_out = 'SSW'
        elif compass_in == 'NE':
            compass_out = 'SW'
        elif compass_in == 'ENE':
            compass_out = 'WSW'
        elif compass_in == 'E':
            compass_out = 'W'
        elif compass_in == 'ESE':
            compass_out = 'WNW'
        elif compass_in == 'SE':
            compass_out = 'NW'
        elif compass_in == 'SSE':
            compass_out = 'NNW'
        elif compass_in == 'S':
            compass_out = 'N'
        elif compass_in == 'SSW':
            compass_out = 'NNE'
        elif compass_in == 'SW':
            compass_out = 'NE'
        elif compass_in == 'WSW':
            compass_out = 'ENE'
        elif compass_in == 'W':
            compass_out = 'E'
        elif compass_in == 'WNW':
            compass_out = 'ESE'
        elif compass_in == 'NW':
            compass_out = 'SE'
        elif compass_in == 'NNW':
            compass_out = 'SSE'
        else:
            compass_out = 'error'
        return compass_out




def mean_confidence_interval(data, confidence=0.95):
	"""Returns the mean value and both confidence intervals of the data provided
	
	First argument is the data we want to calculate the mean confidence interval from.
	The second keyword argument is the confidence level (in parts per unit, (0-1))
	"""
	a = 1.0 * np.array(data)
	n = len(a) 
	m, se = np.mean(a), scipy.stats.sem(a) #GCM# Mean and standard error of an array
	h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1) #GCM# confidence interval value. Obtained as Percent Point Function (Inverse of Cumulative Distribution Function of the Student t distribution)
	return m #GCM# Returns the mean value and both confidence intervals

def bound_confidence_interval(data, confidence=0.95):
	"""Returns the mean value and both confidence intervals of the data provided
	
	First argument is the data we want to calculate the mean confidence interval from.
	The second keyword argument is the confidence level (in parts per unit, (0-1))
	"""
	a = 1.0 * np.array(data)
	n = len(a) 
	m, se = np.mean(a), scipy.stats.sem(a) #GCM# Mean and standard error of an array
	h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1) #GCM# confidence interval value. Obtained as Percent Point Function (Inverse of Cumulative Distribution Function of the Student t distribution)
	return h #GCM# Returns the mean value and both confidence intervals

def plot_pollutant_hour_date(date_value, hour, site, lat_lon_df, pollutants_df, pollutant, traffic_df, run_df):
   #Gives the plot of pollutant concentration for a certain day at a certain hour 
   #shown in Analysis tab

    date_object = date.fromisoformat(date_value)
    date_string = date_object.strftime('%B %d, %Y')
    
    coords_df = lat_lon_df
    df_p = pollutants_df

    poll_df = df_p[(df_p['Date']==date_value)&(df_p["Station"]==site)]
    coords_df = coords_df[coords_df["Station"] == site]
    #pdb.set_trace()
    max_hour = poll_df[poll_df[pollutant] == max(poll_df[pollutant])]['Hour'].to_numpy()[0]

    coords_df = coords_df.sort_values(by='Station')
    poll_df = poll_df.sort_values(by='Hour')

    coords_df[pollutant] = poll_df[(poll_df["Hour"]==hour)][pollutant].to_numpy()[0] 
    #coords_df["Wind Direction (compass)"] =  poll_df[(poll_df["Hour"]==hour)]['Wind Direction (compass)'].to_numpy()[0]
    #pdb.set_trace()
    #run_df['Traffic'] = traffic_df[(traffic_df['Date']==date_value)&(traffic_df['Hour']==hour)].groupby('Runway').size()  
    counts = traffic_df[(traffic_df['Date']==date_value)&(traffic_df['Hour']==hour)].groupby('Runway').Runway.agg('count').to_frame('Traffic').reset_index()
    counts_day = traffic_df[(traffic_df['Date']==date_value)].groupby('Runway').Runway.agg('count').to_frame('Traffic').reset_index()
    for runway in run_df['Runway']:
        if not counts[counts['Runway']==runway].empty:
            flag = run_df['Runway']==runway
            run_df.loc[flag, ['Traffic']] = counts[counts['Runway']==runway]['Traffic'].to_numpy()
    #token = open('mapbox_token').read()
    px.set_mapbox_access_token(open(".mapbox_token").read())
    #Generate figure       
    fig = px.scatter_mapbox(coords_df, lat="lat", lon="lon", color=pollutant,
         hover_name="Station", hover_data=[pollutant],
         color_continuous_scale=["blue", "green", "red"],
         zoom=12, height=400, range_color=[min(poll_df[pollutant]), max(poll_df[pollutant])]) 
    fig.update_layout(mapbox_style="open-street-map") 
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0}) 
    fig.update_layout(title_text='There was a maximum in the concentration of ' + pollutant + ' at ' + site + ' on ' + date_string + ' at  ' + str(max_hour) + 'h' ,
                      title_x=0.1, title_y=.97)
    fig.update_traces(marker=dict(size=12))
    fig.data[0].update(hovertemplate ='<b>%{hovertext}</b><br><br>'+pollutant+'=%{marker.color}<extra></extra>')
    #raw_symbols = SymbolValidator().values
    #pdb.set_trace()
    fig2 = px.scatter_mapbox(run_df, lat=' lat', lon=' lon', color='Traffic',
            color_continuous_scale=["goldenrod", "magenta"],
            hover_name='Runway', hover_data={' lat':False,' lon': False, 'Traffic':True},
            range_color=[min(counts_day['Traffic']), max(counts_day['Traffic'])]) 
    fig2.update_traces(marker=dict(size=20,
                                   colorbar=dict(x=1.5)))#, 
        #line=dict(width=2,
        #          color='DarkSlateGrey')))#, symbol= ['airport', 'airport', 'airport', 'airport'])
  
  
  #fig2.update_traces(marker=dict(symbol= 'airfield', size=20, color='red'))#, symbol= ['airport', 'airport', 'airport', 'airport']))
    #fig2.update_traces(marker_symbol='diamond')
    #fig2.data[0].update(hovertemplate ='<b>%{hovertext}</b><br><br>'+'<extra></extra>')

    #fig.add_trace(fig2.data[0])

  #  fig.update_layout(annotations=[
  #      dict(    
  #          xref= 'x domain',
  #          yref= 'y domain',
  #          x= 0.4,
  #          y= 0.5,
  #          ax=-100,
  #          ay=100,
  #          axref = 'x domain',
  #          ayref = 'y domain',
  #          arrowhead=1,
  #          text = coords_df['Wind Direction (compass)'][0]
  #          )])
  #  sources = {'N' : app.get_asset_url("windroseN.png"),
  #             "NNE" : app.get_asset_url('windroseNNE.png'),
  #             'NE'  : app.get_asset_url('windroseNE.png'),
  #             'ENE'  : app.get_asset_url('windroseNE.png'),
  #             'E'  : app.get_asset_url('windrose.png'),
  #             'ESE'  : app.get_asset_url('windrose.png'),
  #             'SE'  : app.get_asset_url('windrose.png'),
  #             'SSE'  : app.get_asset_url('windrose.png'),
  #             'S'  : app.get_asset_url('windrose.png'),
  #             'SSW'  : app.get_asset_url('windrose.png'),
  #             'SW'  : app.get_asset_url('windrose.png'),
  #             'WSW'  : app.get_asset_url('windrose.png'),
  #             'W'  : app.get_asset_url('windrose.png'),
  #             'WNW'  : app.get_asset_url('windrose.png'),
  #             'NW'  : app.get_asset_url('windrose.png'),
  #             'NNW'  : app.get_asset_url('windrose.png'),
  #             }
  #  key = coords_df['Wind Direction (compass)'][0]
  #  #pdb.set_trace()
  #  fig.add_layout_image(
  #          xref = 'x domain',
  #          yref = 'y domain',
  #          x=0.05,
  #          y=0.9,
  #          sizex =0.2,
  #          sizey=0.2,
  #          source=sources[key]
  #          )
    #pdb.set_trace()
    return fig

def geoloc_stations(lat_lon_df,zoom):
    px.set_mapbox_access_token(open(".mapbox_token").read())
    fig = px.scatter_mapbox(lat_lon_df, lat="lat", lon="lon", text='Station',
            zoom=zoom, height=510, width=670)
    
    #height =510, width=670
    fig.update_layout(mapbox_style='basic')
    #fig.update_traces(marker=dict(size=12, symbol='marker'))
    fig.update_traces(mode='markers+text')
    fig.update_traces(textposition='middle left')
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}) 
    
    return fig


def var_map_date(start_date, end_date, lat_lon_df, pollutants_df, var, zoom):
    # Generates a var (pollutant or noise) by station by date_range figure 
    # INPUT -> two pd.dataframes: 
    # 'lat_lon_df' -> gives latitude and longitude of each station.
    # 'pollutants_df' -> gives sensor measurements @ different stations.
    # OUTPUT -> one figure, px.scatter:
    # fig -> is a plotly fig of the type "open-street-map", 
    #with the mean AQI for the latest month available on the dataset 'pollutants_df' by station.
    
    start_date_object = date.fromisoformat(start_date)
    start_date_string = start_date_object.strftime('%B %d, %Y')
    end_date_object = date.fromisoformat(end_date)
    end_date_string = end_date_object.strftime('%B %d, %Y')

    coords_df = lat_lon_df
    poll_df = pollutants_df

    coords_df = coords_df.sort_values(by='Station')
    poll_df = poll_df.sort_values(by='Date')

    #Filter data by date_range
    poll_df = poll_df[(poll_df['Date']>=start_date) & (poll_df['Date']<=end_date)].groupby('Station').mean()
    coords_df[var] = poll_df[var].round(1)
    coords_df = coords_df.fillna(0)
    coords_df = coords_df.reset_index(drop=True)

    px.set_mapbox_access_token(open(".mapbox_token").read())
    
    #pdb.set_trace()  
    #Generate figure       
    fig = px.scatter_mapbox(coords_df, lat="lat", lon="lon", color=var,
         hover_name="Station", hover_data=[var],
         text = 'Station',
         color_continuous_scale=["blue", "green", "red"],
         zoom=zoom, height= 510, width=670) 
    fig.update_layout(mapbox_style="basic") 
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0}) 
    fig.update_layout(title_text= var + ' from ' + 
                      start_date_string + ' to ' + end_date_string,
                      title_x=0.1, title_y=.97)
    fig.update_traces(marker=dict(size=12))
    fig.update_traces(mode='markers+text')
    fig.update_traces(textposition='middle left')
    #fig.update_traces(hoverinfo='none')
    #fig.update_traces(textfont='Arial Black')
    #fig.update_traces(textfont_color='white')
    #fig.update_traces(textfont_size=14)
    #fig.update_traces(texttemplate = '<b>%{text}</b>')
    #annotations = [
    #        dict(
   
    
    #fig.data[0].update(hovertemplate = '<b>%{hovertext}</b><br><br>AQI=%{marker.color}<extra></extra>')
           
    return fig

def AQI_map_date(start_date, end_date, lat_lon_df, pollutants_df):
    # Generates the AQI by station by date_range figure shown when picking a date_range. 
    # INPUT -> two pd.dataframes: 
    # 'lat_lon_df' -> gives latitude and longitude of each station.
    # 'pollutants_df' -> gives sensor measurements @ different stations.
    # OUTPUT -> one figure, px.scatter:
    # fig -> is a plotly fig of the type "open-street-map", with the mean AQI for the latest month available on the dataset 'pollutants_df' by station.
    
    start_date_object = date.fromisoformat(start_date)
    start_date_string = start_date_object.strftime('%B %d, %Y')
    end_date_object = date.fromisoformat(end_date)
    end_date_string = end_date_object.strftime('%B %d, %Y')

    coords_df = lat_lon_df
    poll_df = pollutants_df

    coords_df = coords_df.sort_values(by='Station')
    poll_df = poll_df.sort_values(by='Date')

    #Filter data by date_range
    poll_df = poll_df[(poll_df['Date']>=start_date) & (poll_df['Date']<=end_date)].groupby('Station').mean()
    coords_df['AQI'] = poll_df[' USAQI'].round(1)
    coords_df = coords_df.fillna(0)
    coords_df = coords_df.reset_index(drop=True)

    px.set_mapbox_access_token(open(".mapbox_token").read())
    
    #pdb.set_trace()  
    #Generate figure       
    fig = px.scatter_mapbox(coords_df, lat="lat", lon="lon", color='AQI',
         hover_name="Station", hover_data=['AQI'],
        text = 'Station',
         color_continuous_scale=["blue", "green", "red"],
         zoom=12.5, height= 510, width=670) 
    fig.update_layout(mapbox_style="basic") 
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0}) 
    fig.update_layout(title_text='Air Quality Index from ' + 
                      start_date_string + ' to ' + end_date_string,
                      title_x=0.1, title_y=.97)
    fig.update_traces(marker=dict(size=12))
    fig.update_traces(mode='markers+text')
    fig.update_traces(textposition='middle left')
    #fig.update_traces(hoverinfo='none')
    #fig.update_traces(textfont='Arial Black')
    #fig.update_traces(textfont_color='white')
    #fig.update_traces(textfont_size=14)
    #fig.update_traces(texttemplate = '<b>%{text}</b>')
    #annotations = [
    #        dict(
   
    
    fig.data[0].update(hovertemplate = '<b>%{hovertext}</b><br><br>AQI=%{marker.color}<extra></extra>')
           
    return fig
def plot_traffic(traffic_df, month):
    # Generates the three figures visible in the traffic tab.
    # INPUT -> one pd.dataframe, desired month string:
    # 'traffic_df' -> traffic dataframe with all currently available data.
    # OUTPUT -> three figures, px.bar:
    # fig -> percentage of flights per terminal for given month.
    # fig2 -> percentage of flights per runway in given month.
    # fig3 -> number of flights per dday in given month colored by runway.

    df = traffic_df
    df_month = df[df['Month']==month] #Keep only data for given month.
    
    pctge_flights_per_terminal = df_month['Air Terminal'].value_counts(normalize=True) * 100
    fig = px.bar(pctge_flights_per_terminal,
             labels={'index' : 'Terminal', 'value': 'Number of Flights [%]'},
             title='Percentage of Flights per Terminal in ' + month)

    pctge_flights_per_runway = df_month['Runway'].value_counts(normalize=True) * 100
    fig2 = px.bar(pctge_flights_per_runway,
             labels={'index' : 'Runway', 'value': 'Number of Flights [%]'},
             title='Percentage of Flights per Runway in ' + month)
        
    pctge_flights_per_runway_day = df_month[['Runway', 'Day of Month']].groupby(['Runway', 'Day of Month']).size().reset_index(name='Number of Flights')
    fig3 = px.bar(pctge_flights_per_runway_day, 
            x='Day of Month', y='Number of Flights', color='Runway',
            title='Number of Flights per Day in ' + month )
    
    return fig, fig2, fig3

def plot_traffic_date(traffic_df, start_date, end_date):
    # Generates the three figures visible in the traffic tab.
    # INPUT -> one pd.dataframe, desired timerange:
    # 'traffic_df' -> traffic dataframe with all currently available data.
    # OUTPUT -> three figures, px.bar:
    # fig -> percentage of flights per terminal for given period.
    # fig2 -> percentage of flights per runway in given period.
    # fig3 -> number of flights per dday in given period colored by runway.

    start_date_object = date.fromisoformat(start_date)
    start_date_string = start_date_object.strftime('%B %d, %Y')
    end_date_object = date.fromisoformat(end_date)
    end_date_string = end_date_object.strftime('%B %d, %Y')
    
    df = traffic_df.sort_values(by='Date')
    df_month = df[(df['Date']>=start_date) & (df['Date']<=end_date)] #Keep only data for given timeperiod.
    
    pctge_flights_per_terminal = df_month['Air Terminal'].value_counts(normalize=True) * 100
    fig = px.bar(pctge_flights_per_terminal,
             labels={'index' : 'Terminal', 'value': 'Number of Flights [%]'},
             title='Percentage of Flights per Terminal from ' + start_date_string + ' to ' +
             end_date_string)
    pdb.set_trace()
    pctge_flights_per_runway = df_month['Runway'].value_counts(normalize=True) * 100
    fig2 = px.bar(pctge_flights_per_runway,
             labels={'index' : 'Runway', 'value': 'Number of Flights [%]'},
             title='Percentage of Flights per Runway from ' + start_date_string + ' to ' +
             end_date_string)
        
    pctge_flights_per_runway_day = df_month[['Runway', 'Day of Month']].groupby(['Runway', 'Day of Month']).size().reset_index(name='Number of Flights')
    fig3 = px.bar(pctge_flights_per_runway_day, 
            x='Day of Month', y='Number of Flights', color='Runway',
            title='Number of Flights per Day from ' + start_date_string + ' to ' +
            end_date_string)
    
    
    return fig, fig2, fig3
def plot_pollutant_date(site, start_date, end_date, pollutant, poll_df):
    # Generates the two figures shown in the AQI (pollutants) section.
    # INPUT -> three strings and one pd.dataframe:
    # 'site' -> query of the desired site.
    # 'month' -> query of the desired month.
    # 'pollutant' -> query of desired pollutant.
    # 'poll_df' -> pd.dataframe with all available pollutant data.
    # OUTPUT -> two figures, px.scatter:
    # fig -> 1 by 3 subplot of  mean bounded by std_deviation of a given pollutant.
    #        The format is |Hourly|Monthly|Weekday|. i.e. for the 1st subplot the logic is:
    #        in a given month whats the mean concentration of "CO_2" (e.g.) at "5 pm" (e.g.).
    # fig1 -> 1 by 7 subplot of mean bounded by std_deviation of a given pollutant for a day in the
    #         week belonging to that month. 
    #         The format is: |Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|
    #         x-axis: hour of the day, y-axis: concentration.

    #Prepare datasets
    df = poll_df.sort_values(by='Date').reset_index(drop=True)
    df = df[(df['Date']>=start_date) & (df['Date']<=end_date)]
    df_s = poll_df
    df_s = df_s[df_s['Station']==site]
    df = df[(df['Station']==site)]
 
    pollutants = ['Temperature (°C)', 'R. Humidity (%)',  
            'CO (mg/m³)','NO₂ (µg/m³ )','O₃ (µg/m³ )','SO₂ (µg/m³)',
            'PM₂.₅ (µg/m³ )','PM₁₀ (µg/m³)',#'PM₁ (µg/m³ )', 
            'CO₂ (ppm)',
            'H₂S (µg/m³ )', 'NO (µg/m³ )','Leq (dB)', 'Lmin (dB)', 'Lmax (dB)']


    #Logic for retriveing days and months ordered humanly and not alphabetically.
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    months_index = poll_df['Month Index'].unique()
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 
              'November', 'December']
    months = months[0:max(months_index)]
    #pdb.set_trace()
    cat_days = CategoricalDtype(categories=days, ordered=True)
    cat_months = CategoricalDtype(categories=months, ordered=True)
    df_s["Day"] = df_s["Day"].astype(cat_days)
    df_s["Month"] = df_s["Month"].astype(cat_months)
    df["Day"] = df["Day"].astype(cat_days)
    
    fig = make_subplots(
            rows=1, cols=3,
            subplot_titles=("Hourly", "Monthly",
                            "Weekday"),
            shared_yaxes=True)
    
    fig1 = make_subplots(
             rows=1, cols=7,
             subplot_titles=days,
             shared_yaxes=True)

    sort_labels = ['Hour', 'Month Index', 'Day Index']
 
 
    df_s[pollutants] = df_s[pollutants].astype(float)
    df[pollutants] = df[pollutants].astype(float)
    for i, query in enumerate(['Hour', 'Month','Day']):
        #pdb.set_trace()
        if i==1:
            #df_mean = df_s.groupby(query, as_index=False)[pollutants].mean()
            df_mean = df_s.groupby(query, as_index=False)[pollutants].\
                    agg(mean_confidence_interval)
            df_std = df_s.groupby(query)[pollutants].\
                    agg(bound_confidence_interval).reset_index()        
            #df_std  = df_s.groupby(query)[pollutants].std(ddof=0).reset_index()
            #df_std = df_s.groupby(query)[pollutants].quantile(q=.95)
        elif i==2:
            #df_mean = df.groupby(query, as_index=False)[pollutants].mean()
            df_mean = df.groupby(query,as_index=False)[pollutants].\
                    agg(mean_confidence_interval)
            df_std = df.groupby(query)[pollutants].\
                    agg(bound_confidence_interval).reset_index()        
            #df_std  = df.groupby(query)[pollutants].std(ddof=0).reset_index()
            #df_std = df_s.groupby(query)[pollutants].quantile(q=.95)
        else:
            #df_mean = df.groupby(query, as_index=False)[pollutants].mean()
            df_mean = df.groupby(query,as_index=False)[pollutants].\
                    agg(mean_confidence_interval)
            df_std = df.groupby(query)[pollutants].\
                    agg(bound_confidence_interval).reset_index()        
            #pdb.set_trace()
            #df_std  = df.groupby(query)[pollutants].std(ddof=0).reset_index()
            #df_std = df_s.groupby(query)[pollutants].quantile(q=.95)
        
        if query == 'Month' or query=='Day':
           # fig.add_trace(go.Scatter(
           #     name='Measurement',
           #     x=df_mean[query],
           #     y=df_mean[pollutant],
           #     mode='lines+markers',
           #     line=dict(color='rgb(31, 119, 180)'),
           #     showlegend=False),
           #     row=1,col=i+1)
           #pdb.set_trace()
           fig.add_trace(go.Scatter(
               #name='Measurement',
               x=df_mean[query],
               y=df_mean[pollutant],
               line=dict(color='rgb(31, 119, 180)'),
               error_y=dict(
                   type='data',
                   array=df_std[pollutant],
                   color='#444',
                   visible=True),
               showlegend=False),
               row=1,col=i+1)
               
        else:
            fig.add_trace(go.Scatter(
                name='Measurement',
                x=df_mean[query],
                y=df_mean[pollutant],
                mode='lines',
                line=dict(color='rgb(31, 119, 180)'),
                showlegend=False),
                row=1,col=i+1)
             
            fig.add_trace(go.Scatter(
                name='Upper Bound',
                x=df_mean[query],
                y=df_mean[pollutant]+df_std[pollutant],
                mode='lines',
                marker=dict(color="#444"),
                line=dict(width=0),
                showlegend=False),
                row=1,col=i+1) 
            
            
            
            df_low_bound = df_mean[pollutant]-df_std[pollutant]
            df_low_bound[df_low_bound <0]=0

            fig.add_trace(go.Scatter(
                name='Lower Bound',
                x=df_mean[query],
                y=df_low_bound,
                marker=dict(color="#444"),
                line=dict(width=0),
                mode='lines',
                fillcolor='rgba(68, 68, 68, 0.3)',
                fill='tonexty',
                showlegend=False),
                row=1,col=i+1)
          #Update yaxis props

    
    for j, day in enumerate(days):    
        df_d = df[df['Day']==day]
        #pdb.set_trace() 
        if not df_d.empty:
            query = 'Hour'
            #df_mean = df_d.groupby(query, as_index=False)[pollutants].mean()
            df_mean = df_d.groupby(query,as_index=False)[pollutants].\
                    agg(mean_confidence_interval)
            df_std = df_d.groupby(query)[pollutants].\
                    agg(bound_confidence_interval).reset_index()        
            #df_std  = df_d.groupby(query)[pollutants].std(ddof=0).reset_index()
            #df_std = df_d.groupby(query)[pollutants].quantile(q=.95)
 
            fig1.add_trace(go.Scatter(
                name='Measurement',
                x=df_mean[query],
                y=df_mean[pollutant],
                mode='lines',
                line=dict(color='rgb(31, 119, 180)'),
                showlegend=False),
                row=1,col=j+1)
            fig1.add_trace(go.Scatter(
                name='Upper Bound',
                x=df_mean[query],
                y=df_mean[pollutant]+df_std[pollutant],
                mode='lines',
                marker=dict(color="#444"),
                line=dict(width=0),
                showlegend=False),
                row=1,col=j+1) 
            df_low_bound = df_mean[pollutant]-df_std[pollutant]
            df_low_bound[df_low_bound <0]=0
            
            fig1.add_trace(go.Scatter(
               name='Lower Bound',
               x=df_mean[query],
               y=df_low_bound,
               marker=dict(color="#444"),
               line=dict(width=0),
               mode='lines',
               fillcolor='rgba(68, 68, 68, 0.3)',
               fill='tonexty',
               showlegend=False),
               row=1,col=j+1)
            
    fig.update_yaxes(title_text='Avg ' + pollutant, row=1,col=1)
    fig.update_xaxes(title_text='Hour', row=1, col=1)
    fig.update_layout(
      # yaxis_title='Avg ' + pollutant,
      # title='Measurements at: ' + site + ' in '+month,
       hovermode="x"
       )
    fig1.update_layout(title='Site: ' + site)
    
    fig.update_layout(margin={"t": 25, "b":5})
    fig1.update_layout(margin={"b":8}) 
    fig1.update_yaxes(title_text='Avg ' + pollutant, row=1,col=1)
    fig1.update_xaxes(title_text='Hour', row=1, col=4)
    fig1.update_layout(
      # yaxis_title='Avg ' + pollutant,
      # title='Measurements at: ' + site + ' in '+month,
       hovermode="x"
       )

    return fig, fig1

def plot_traffic_bars(start_date, end_date, traff_df):
    # Generates the two figures shown in the AQI (pollutants) section.
    # INPUT -> three strings and one pd.dataframe:
    # 'site' -> query of the desired site.
    # 'month' -> query of the desired month.
    # 'pollutant' -> query of desired pollutant.
    # 'traff_df' -> pd.dataframe with all available pollutant data.
    # OUTPUT -> two figures, px.scatter:
    # fig -> 1 by 3 subplot of  mean bounded by std_deviation of a given pollutant.
    #        The format is |Hourly|Monthly|Weekday|. i.e. for the 1st subplot the logic is:
    #        in a given month whats the mean concentration of "CO_2" (e.g.) at "5 pm" (e.g.).
    # fig1 -> 1 by 7 subplot of mean bounded by std_deviation of a given pollutant for a day in the
    #         week belonging to that month. 
    #         The format is: |Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|
    #         x-axis: hour of the day, y-axis: concentration.

    #Prepare datasets
    df = traff_df.sort_values(by='Date').reset_index(drop=True)
    df = df[(df['Date']>=start_date) & (df['Date']<=end_date)]
    df_s = traff_df
    
    
 


    #Logic for retriveing days and months ordered humanly and not alphabetically.
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    months_index = traff_df['Month Index'].unique()
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 
              'November', 'December']
    months = months[0:max(months_index)]
    #pdb.set_trace()
    cat_days = CategoricalDtype(categories=days, ordered=True)
    cat_months = CategoricalDtype(categories=months, ordered=True)
    df_s["Day"] = df_s["Day"].astype(cat_days)
    df_s["Month"] = df_s["Month"].astype(cat_months)
    
    fig = make_subplots(
            rows=1, cols=3,
            subplot_titles=("Hourly", "Monthly",
                            "Weekday"),
            shared_yaxes=False)
    
    fig1 = make_subplots(
             rows=1, cols=7,
             subplot_titles=days,
             shared_yaxes=True)

    sort_labels = ['Hour', 'Month Index', 'Day Index']
 
 
    #df_s[pollutants] = df_s[pollutants].astype(float)
    #df[pollutants] = df[pollutants].astype(float)
    for i, query in enumerate(['Hour', 'Month','Day']):
        #pdb.set_trace()
        if i==1:
            df_count = df_s.groupby(query, as_index=False)['To Date'].count()
            #pdb.set_trace() 
            #pdb.set_trace
        elif i==2:
            df_count = df.groupby(query, as_index=False)['To Date'].count()
        else:
            df_count = df.groupby(query, as_index=False)['To Date'].count()
            #pdb.set_trace()
          
        #df_count = df_count.rename(columns={'To Date': 'Operation count'})
        fig.add_trace(go.Bar(
            name='Measurement',
            x=df_count[query],
            y=df_count['To Date']),
            row=1,col=i+1)


    
    for j, day in enumerate(days):    
        df_d = df[df['Day']==day]
        #pdb.set_trace() 
        if not df_d.empty:
            query = 'Hour'
            df_count = df_d.groupby(query, as_index=False)['To Date'].count()
           #df_count = df_count.rename(columns={'To Date': 'Operation count'})

            fig1.add_trace(go.Bar(
                name='Measurement',
                x=df_count[query],
                y=df_count['To Date']),
                row=1,col=j+1)
            
    fig.update_yaxes(title_text='Operation count', row=1,col=1)
    fig.update_xaxes(title_text='Hour', row=1, col=1)
    fig.update_layout(
      # yaxis_title='Avg ' + pollutant,
      # title='Measurements at: ' + site + ' in '+month,
       hovermode="x"
       )
    #fig1.update_layout(title='Site: ' + site)
    fig.update_layout(showlegend=False)
    fig1.update_layout(showlegend=False)
    fig1.update_yaxes(title_text='Operation count', row=1,col=1)
    fig1.update_xaxes(title_text='Hour', row=1, col=4)
    fig1.update_layout(
      # yaxis_title='Avg ' + pollutant,
      # title='Measurements at: ' + site + ' in '+month,
       hovermode="x"
       )

    return fig, fig1
def plot_pollutant(site, month, pollutant, poll_df):
    # Generates the two figures shown in the AQI (pollutants) section.
    # INPUT -> three strings and one pd.dataframe:
    # 'site' -> query of the desired site.
    # 'month' -> query of the desired month.
    # 'pollutant' -> query of desired pollutant.
    # 'poll_df' -> pd.dataframe with all available pollutant data.
    # OUTPUT -> two figures, px.scatter:
    # fig -> 1 by 3 subplot of  mean bounded by std_deviation of a given pollutant.
    #        The format is |Hourly|Monthly|Weekday|. i.e. for the 1st subplot the logic is:
    #        in a given month whats the mean concentration of "CO_2" (e.g.) at "5 pm" (e.g.).
    # fig1 -> 1 by 7 subplot of mean bounded by std_deviation of a given pollutant for a day in the
    #         week belonging to that month. 
    #         The format is: |Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|
    #         x-axis: hour of the day, y-axis: concentration.

    #Prepare datasets
    df = poll_df
    df_s = df[df['Station']==site]
    df = df[(df['Month']==month) & (df['Station']==site)]
    

    #Logic for retriveing days and months ordered humanly and not alphabetically.
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    months_index = poll_df['Month Index'].unique()
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
              'September', 'October', 'November', 'December']
    months = months[0:max(months_index)]
    
    cat_days = CategoricalDtype(categories=days, ordered=True)
    cat_months = CategoricalDtype(categories=months, ordered=True)
    df_s["Day"] = df_s["Day"].astype(cat_days)
    df_s["Month"] = df_s["Month"].astype(cat_months)
    
    fig = make_subplots(
            rows=1, cols=3,
            subplot_titles=("Hourly", "Monthly",
                            "Weekday"))
    
    fig1 = make_subplots(
             rows=1, cols=7,
             subplot_titles=days)

    sort_labels = ['Hour', 'Month Index', 'Day Index']
    for i, query in enumerate(['Hour', 'Month','Day']):
        if i==1:
            df_mean = df_s.groupby(query, as_index=False).mean()
            df_std  = df_s.groupby(query, as_index=False).std()
        elif i==2:
            df_mean = df_s.groupby(query, as_index=False).mean()
            df_std  = df_s.groupby(query, as_index=False).std()
        else:
            df_mean = df.groupby(query, as_index=False).mean()
            df_std  = df.groupby(query, as_index=False).std()
          
        fig.add_trace(go.Scatter(
            name='Measurement',
            x=df_mean[query],
            y=df_mean[pollutant],
            mode='lines',
            line=dict(color='rgb(31, 119, 180)'),
            showlegend=False),
            row=1,col=i+1)

        fig.add_trace(go.Scatter(
            name='Upper Bound',
            x=df_mean[query],
            y=df_mean[pollutant]+df_std[pollutant],
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False),
            row=1,col=i+1) 
        
        fig.add_trace(go.Scatter(
            name='Lower Bound',
            x=df_mean[query],
            y=df_mean[pollutant]-df_std[pollutant],
            marker=dict(color="#444"),
            line=dict(width=0),
            mode='lines',
            fillcolor='rgba(68, 68, 68, 0.3)',
            fill='tonexty',
            showlegend=False),
            row=1,col=i+1)
          #Update yaxis props
        
    for j, day in enumerate(days):    
        df_d = df[df['Day']==day]
        query = 'Hour'
        df_mean = df_d.groupby(query, as_index=False).mean()
        df_std  = df_d.groupby(query, as_index=False).std()

        fig1.add_trace(go.Scatter(
            name='Measurement',
            x=df_mean[query],
            y=df_mean[pollutant],
            mode='lines',
            line=dict(color='rgb(31, 119, 180)'),
            showlegend=False),
            row=1,col=j+1)

        fig1.add_trace(go.Scatter(
            name='Upper Bound',
            x=df_mean[query],
            y=df_mean[pollutant]+df_std[pollutant],
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False),
            row=1,col=j+1) 
      
        fig1.add_trace(go.Scatter(
           name='Lower Bound',
           x=df_mean[query],
           y=min(df_mean[pollutant]-df_std[pollutant], 0),
           marker=dict(color="#444"),
           line=dict(width=0),
           mode='lines',
           fillcolor='rgba(68, 68, 68, 0.3)',
           fill='tonexty',
           showlegend=False),
           row=1,col=j+1)
            
    fig.update_yaxes(title_text='Avg ' + pollutant, row=1,col=1)
    #fig.update_xaxes(automargin=True, row=1, col=3)
    fig.update_layout(
          # yaxis_title='Avg ' + pollutant,
      # title='Measurements at: ' + site + ' in '+month,
       hovermode="x"
       )
    
    fig1.update_yaxes(title_text='Avg ' + pollutant, row=1,col=1)
    fig1.update_layout(
      # yaxis_title='Avg ' + pollutant,
      # title='Measurements at: ' + site + ' in '+month,
       hovermode="x"
       )

    return fig, fig1

def find_pollutant_max(pollutant, start_date, end_date, poll_df):
    # For a desired pollutant find the max concentration on a given timeframe.
    df = poll_df.sort_values(by='Date')
    df = df[(df['Date']>=start_date) & (df['Date']<=end_date)]
    maxi = df[df[pollutant] == df[pollutant].max()]
    site = maxi['Station'].reset_index(drop=True).get(0)
    day = maxi['Date'].reset_index(drop=True).get(0)
    return site, day


def plot_analysis(site, date_value, pollutant, traffic_df, poll_df):
    # Generates the figure shown in the analysis tab.
    # INPUT: three strings, two pd.dataframes.
    # 'site' -> query of desired site.
    # 'date_value' -> query of desired date.
    # 'pollutant' -> query of desired pollutant.
    # 'traffic_df' -> dataframe with all available traffic data.
    # 'poll_df' -> dataframe with all available pollutant data.
    # OUTPUT: one figure, complicated two axis with px.bar and px.line.
    # fig -> plots the

        
    #Get date information  
    df_t = traffic_df
    date_object = date.fromisoformat(date_value)
    df_p = poll_df
    date_string = date_object.strftime('%B %d, %Y')
    
    
    nbr_flights_per_hour_runway = df_t[df_t['Date']==date_value].groupby(['Hour','Runway']).size().reset_index(name='Number of Flights')
    
    subfig = make_subplots(specs=[[{"secondary_y": True}]])

    fig = px.bar(nbr_flights_per_hour_runway, x='Hour', y='Number of Flights', color='Runway')
    
    poll_per_station=df_p[(df_p['Date']==date_value)&(df_p["Station"]==site)]
    #pdb.set_trace()
    
    fig2=px.line(poll_per_station,x="Hour", y=pollutant)
    
    fig2['data'][0]['showlegend']=True
    fig2['data'][0]['name']=pollutant
    
    #Format axis
    fig2.update_traces(yaxis='y2')
    fig2.update_traces(mode='markers+lines')
    fig2.update_traces(line_color='goldenrod')
    subfig.add_traces(fig.data + fig2.data)
    subfig.layout.xaxis.title="Hour"
    subfig.layout.yaxis.title="Number of Flights"
    subfig.layout.yaxis2.title=pollutant
    subfig.layout.barmode='stack'
    subfig.update_layout(title='Max of ' + pollutant + ' at ' + site + ' on ' + date_string)

    return subfig

def plot_pollutant_all_stations(month, pollutant, poll_df):
    
    poll_df = poll_df[poll_df['Month'] == month]
    poll_df = poll_df.sort_values(['To Date']).reset_index(drop=True)
    fig = px.line(poll_df, x = 'To Date', y = pollutant, color = 'Station', labels={'x':'Date'})
    fig.update_xaxes(tickmode = 'array',
                     ticktext = poll_df['Date'].to_numpy())
    return fig

def plot_pollutant_all_stations_date(start_date, end_date, pollutant, poll_df):
    
    poll_df = poll_df.sort_values(by='Date')
    poll_df = poll_df[(poll_df['Date']>=start_date) & (poll_df['Date']<=end_date)]
    #poll_df = poll_df[poll_df['Month'] == month]
    poll_df = poll_df.sort_values(['To Date']).reset_index(drop=True)
    fig = px.line(poll_df, x = 'To Date', y = pollutant, color = 'Station')
    #fig.layout.xaxis.tickmode = 'array'
    #fig.layout.xaxis.ticktext = poll_df['Date']
    fig.layout.xaxis.nticks = 10

    return fig

def plot_pollutant_multi_stations_date(start_date, end_date, pollutant, poll_df, stations, 
        limits_df, title):
    poll_df = poll_df.sort_values(by='Date').reset_index(drop=True)
    poll_df = poll_df[(poll_df['Date']>=start_date) & (poll_df['Date']<=end_date) & 
            (poll_df['Station'].isin(stations))]
    #poll_df = poll_df[poll_df['Month'] == month]
    poll_df = poll_df.sort_values(['To Date']).reset_index(drop=True)
    #pdb.set_trace()
    #poll_df['Ordinal'] = pd.to_datetime(poll_df['To Date']).apply(lambda x: x.to_julian_date())
    poll_df['To Date'] = pd.to_datetime(poll_df['To Date'], dayfirst=True)
    
    fig = px.line(poll_df, x = 'To Date', y = pollutant, color = 'Station')
    
    
    #fig.layout.xaxis.tickmode = 'array'
    #fig.layout.xaxis.ticktext = poll_df['To Date']
    fig.layout.xaxis.nticks = 10
    #fig.layout.xaxis.type = 'category'
    #x_0 = poll_df['To Date'].min()
    #x_f = poll_df['To Date'].max()
    #add Limit
    #fig.update_xaxes(tickformat='%b\n%Y`')
    lim = limits_df[limits_df['Pollutant'] == pollutant]['Level']
    fig.update_layout(title=title + ' for ' + pollutant)
    #pdb.set_trace()
    if not lim.empty:
        lim = lim.to_numpy()[0]
        fig.add_hline(y=lim, line_color='red', annotation_text='Limit')
    

    return fig

#def plot_windrose(site, date_value, poll_df):
#    directions = poll_df['Wind Direction (compass)'].unique()
#    poll_df = poll_df[(poll_df['Date']==date_value) & (poll_df['Station']==site)]
#    wrose_df = poll_df[['Wind Speed (km/h)', 'Wind Direction (compass)']]
#    wrose_df = wrose_df.groupby(['Wind Speed (km/h)', 'Wind Direction (compass)']).size().reset_index(name='Frequency') 
#
#    fig = px.bar_polar(wrose_df, r='Frequency', theta='Wind Direction (compass)',
#                 color='Wind Speed (km/h)')
#
#    #ig.layout.polar.angularaxis.tickvals=[0, 45, 90, 135, 180, 225, 270, 315]
#    fig.layout.polar.angularaxis.rotation=0
#    fig.layout.polar.angularaxis.direction='counterclockwise'
#    fig.layout.polar.angularaxis.categoryorder='array'
#    fig.layout.polar.angularaxis.categoryarray = np.array(['E', 'ENE', 'NE', 'NNE', 'N', 
#        'NNW', 'NW', 'WNW', 'W', 'WSW', 'SW', 'SSW', 'S', 'SSE', 'SE', 'ESE'])
#    return fig 

def plot_windrose(site, date_value, poll_df):
    poll_df = poll_df[(poll_df['Date']==date_value) & (poll_df['Station']==site)]
    wr_df = poll_df[['Wind Speed (km/h)',  'Wind Direction (degree)']]
    names = { 'Wind Speed (km/h)': 'ws',  'Wind Direction (degree)':'wd'}
    wr_df[wr_df['Wind Speed (km/h)']<0] = 0
    WR = WindRose(wr_df)
    WR.calc_stats(normed=True, bins=6, variable_names=names)
    WR.wind_df = WR.wind_df.sort_values(by='speed')
    #fig = px.bar_polar(df,r='frequency',theta='direction',color='speed',
    #                color_discrete_sequence= px.colors.sequential.Plasma_r)
    fig=WR.plot(output_type='return', template='plotly', colors='Plasma')
    fig.update_layout(margin={"r":0,"l":18,"t":18,"b":18})
    return fig 

def plot_windrose_date(site, start_date, end_date, poll_df):
    poll_df = poll_df[(poll_df['Date']>=start_date) &\
            (poll_df['Date']<=end_date) & (poll_df['Station']==site)] 
    wr_df = poll_df[['Wind Speed (km/h)',  'Wind Direction (degree)']]
    names = { 'Wind Speed (km/h)': 'ws',  'Wind Direction (degree)':'wd'}
    wr_df[wr_df['Wind Speed (km/h)']<0] = 0
    WR = WindRose(wr_df)
    WR.calc_stats(normed=True, bins=6, variable_names=names)
    WR.wind_df = WR.wind_df.sort_values(by='speed')
    
    #fig = px.bar_polar(df,r='frequency',theta='direction',color='speed',
    #                color_discrete_sequence= px.colors.sequential.Plasma_r)

    fig=WR.plot(output_type='return', template='plotly', colors='Plasma')
    fig.update_layout(margin={"r":0,"l":18,"t":0,"b":0})
    return fig 

#def plot_windrose_date(site, start_date, end_date, poll_df):
#    directions = poll_df['Wind Direction (compass)'].unique()
#    #pdb.set_trace()
#    poll_df = poll_df[(poll_df['Date']>=start_date) & (poll_df['Date']<=end_date) & (poll_df['Station']==site)]                  
#    
#    wrose_df = poll_df[['Wind Speed (km/h)', 'Wind Direction (compass)']]
#    wrose_df = wrose_df.groupby(['Wind Speed (km/h)', 'Wind Direction (compass)']).size().reset_index(name='Frequency') 
#
#    fig = px.bar_polar(wrose_df, r='Frequency', theta='Wind Direction (compass)',
#                 color='Wind Speed (km/h)')
#
#    #fig.layout.polar.angularaxis.tickvals=[0, 45, 90, 135, 180, 225, 270, 315]
#    fig.layout.polar.angularaxis.rotation=0
#    fig.layout.polar.angularaxis.direction='counterclockwise'
#    fig.layout.polar.angularaxis.categoryorder='array'
#    fig.layout.polar.angularaxis.categoryarray = np.array(['E', 'ENE', 'NE', 'NNE', 'N', 
#        'NNW', 'NW', 'WNW', 'W', 'WSW', 'SW', 'SSW', 'S', 'SSE', 'SE', 'ESE'])
#    
#    fig.update_layout(margin={"r":0,"l":18,"t":0,"b":0}) 
#    return fig 

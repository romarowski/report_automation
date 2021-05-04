from modules import coordinates, transforms_pollutants, transforms_traffic
from modules.plotting import *
import os
import pdb
from PIL import Image, ImageDraw
from pandas.api.types import CategoricalDtype
# Asign databases, variables to meaningful names

def make_plots(start_date, end_date):

    oneHourPoll = transforms_pollutants.data
    eightHourPoll = transforms_pollutants.data8
    twofourHourPoll = transforms_pollutants.data24
    trafficDF = transforms_traffic.data
    limitsDF = transforms_pollutants.limits
    coords_df = coordinates.coords_df

    if not os.path.exists("images"):
        os.mkdir("images")
    pollutants = ['CO (mg/m³)','NO₂ (µg/m³ )','O₃ (µg/m³ )','SO₂ (µg/m³)',
            'PM₂.₅ (µg/m³ )','PM₁₀ (µg/m³)',#'PM₁ (µg/m³ )', 
            'CO₂ (ppm)',
            'H₂S (µg/m³ )', 'NO (µg/m³ )','Leq (dB)', 'Lmin (dB)', 'Lmax (dB)']

    noises = ['Leq (dB)', 'Lmin (dB)', 'Lmax (dB)']
    meteos = ['Temperature (°C)', 'R. Humidity (%)']
    sites = sorted(oneHourPoll['Station'].unique(), key=str.casefold)
    #pollutants = ['PM₁ (µg/m³ )', 'CO₂ (ppm)']

    #Pick dates

    #start_date = '2021-03-01'
    #end_date = '2021-03-31'



    print('Processing monthly windrose...')
    fig = plot_windrose_date('Privet Aviation', start_date, end_date, oneHourPoll)
    fig.write_image('images/windrosemonth.png', height=600, width=600)




    print('Processing operations fig...')
    figA, figB  = plot_traffic_bars(start_date, end_date,
                                                   trafficDF)
    figA.write_image('images/trafficA.png',
                scale=1.0, width=1200, height=500)
    figB.write_image('images/trafficB.png', 
                scale=1.0, width=1200, height=500)
    image1 = Image.open('images/trafficB.png')
    image2 = Image.open('images/trafficA.png')
    image1_size = image1.size
    image2_size = image2.size
    draw = ImageDraw.Draw(image1)
    draw.line((0,image1_size[1], image1_size[0], image1_size[1]), fill=128, width=3)
    new_image = Image.new('RGB',(image1_size[0], 2*image1_size[1]), (250, 250, 250))
    new_image.paste(image1, (0,0))
    new_image.paste(image2,(0, image1_size[1]))
    new_image.save('images/traffic.png', 'PNG')
    os.remove('images/trafficA.png')
    os.remove('images/trafficB.png')




    # Position of stations
    print('Processing station position fig...')
    figGeo = geoloc_stations(coords_df.head(8), zoom=12.5)
    figGeo.write_image('images/map1.png')
    figGeo = geoloc_stations(coords_df.tail(5), zoom=11.4)
    figGeo.write_image('images/map2.png')




    # Noise figures
    print('Processing noise figs...')
    i = 1
    flag = oneHourPoll['Station'].isin(coords_df.head(8)['Station'].to_numpy())

    for noise in noises:
        figNoise = var_map_date(start_date, end_date, coords_df.head(8),
                oneHourPoll[flag], noise, zoom=12.5)
        figNoise.write_image('images/image' + str(i) + '.png')
        i += 1

    flag = oneHourPoll['Station'].isin(coords_df.tail(5)['Station'].to_numpy())

    for noise in noises:
        figNoise = var_map_date(start_date, end_date, coords_df.tail(5), oneHourPoll[flag], noise, zoom=11.4)
        figNoise.write_image('images/image' + str(i) + '.png')
        i += 1




    # Traffic figures

    print('Processing trafic figs...')
    figTrafficTerminal, figTrafficRunway,\
    figTrafficRunwayDaily = plot_traffic_date(trafficDF, 
                                              start_date,
                                              end_date)
    figTrafficTerminal.write_image('images/image'+str(i)+'.png')#, 
            #scale=1.0, width=1200, height=1800)
    i+=1
    figTrafficRunway.write_image('images/image'+str(i)+'.png')#, 
            #scale = 1.0, width=1200, height=1800)
    i+=1
    figTrafficRunwayDaily.write_image('images/image'+str(i)+'.png')#, 
            #scale = 1.0, width=1200, height=1800)
    i+=1




    # Maximum per pollutant 

    #i=13 #set counter for images
    print('Processing analysis figs...')
    for poll in pollutants:

        site, day = find_pollutant_max(poll, start_date, end_date, oneHourPoll)
        figMaxPoll = plot_analysis(site, day, poll, trafficDF, oneHourPoll)
        figMaxPoll.write_image('images/image' + str(i) + '.png')#,
        #        scale = 1.0, width=1200, height=1800)
        figWindrose = plot_windrose(site, day, oneHourPoll)
        figWindrose.write_image('images/windrose'+poll.split(' ')[0]+'.png')#, 
         #       scale = 1.0, width=1200, height=1800)
        i += 1




    # Average AQI
    print('Processing AQI figs...')
    flag = oneHourPoll['Station'].isin(coords_df.head(8)['Station'].to_numpy())

    figAQI = var_map_date(start_date, end_date, coords_df.head(8), oneHourPoll[flag], var=' USAQI', zoom=12.5)
    #figAQI.show()
    figAQI.write_image('images/image'+str(i)+'.png',scale=1.0)#,
            #width=1200, height=1800)
    i +=1





    flag = oneHourPoll['Station'].isin(coords_df.tail(5)['Station'].to_numpy())

    figAQI = var_map_date(start_date, end_date, coords_df.tail(5), oneHourPoll[flag], var=' USAQI', zoom=11.4)
    #figAQI.show()
    figAQI.write_image('images/image'+str(i)+'.png',scale=1.0)#,
            #width=1200, height=1800)
    i +=1



    # Meteorological graphs
    print('Processing meteo figs...')
    site='Privet Aviation'
    i = 24
    for pollutant in meteos:
        figPollA, figPollB  = plot_pollutant_date(site, start_date, end_date,
                                                  pollutant, oneHourPoll)
        figPollA.write_image('images/image'+str(i)+'A.png',
                scale=1.0, width=800, height=250)
        figPollB.write_image('images/image'+str(i)+'B.png', 
                scale=1.0, width=800, height=250)
        image1 = Image.open('images/image'+str(i)+'B.png')
        image2 = Image.open('images/image'+str(i)+'A.png')
        draw = ImageDraw.Draw(image1)
        image1_size = image1.size
        image2_size = image2.size
        draw.line((0,image1_size[1], image1_size[0], image1_size[1]), fill=128, width=3)
        new_image = Image.new('RGB',(image1_size[0], 2*image1_size[1]), (250, 250, 250))
        new_image.paste(image1, (0,0))
        new_image.paste(image2,(0, image1_size[1]))
        new_image.save('images/image'+str(i)+'.png', 'PNG')
        os.remove('images/image'+str(i)+'A.png')
        os.remove('images/image'+str(i)+'B.png')
        i += 1




    # Charts by Station and pollutant
    print('Processing grouped pollutant figs...')

    #i=31

    #pdb.set_trace()
    for site in sites:
        for pollutant in pollutants:
            if not oneHourPoll[(oneHourPoll['Station']==site) &
                               (oneHourPoll['Date']>=start_date) &
                               (oneHourPoll['Date']<=end_date)][pollutant].empty:           

                figPollA, figPollB  = plot_pollutant_date(site, start_date, end_date,
                                                          pollutant, oneHourPoll)
                figPollA.write_image('images/image'+str(i)+'A.png',
                       scale=1.0, width=800, height=250)
                figPollB.write_image('images/image'+str(i)+'B.png', 
                        scale=1.0, width=800, height=250)
                image1 = Image.open('images/image'+str(i)+'B.png')
                image2 = Image.open('images/image'+str(i)+'A.png')
                image1_size = image1.size
                image2_size = image2.size
                draw = ImageDraw.Draw(image1)
                draw.line((0,image1_size[1], image1_size[0], image1_size[1]),
                        fill=128, width=3)
                new_image = Image.new('RGB',(image1_size[0], 2*image1_size[1]),
                        (250, 250, 250))
                new_image.paste(image1, (0,0))
                new_image.paste(image2,(0, image1_size[1]))
                new_image.save('images/image'+str(i)+'.png', 'PNG')
                os.remove('images/image'+str(i)+'A.png')
                os.remove('images/image'+str(i)+'B.png')
                i += 1




    print('Processing pollutants with limits plots')
    #i =187
    sep_sites = [sites[0:3], sites[3:6], sites[6:9], sites[9:13]]
    #pdb.set_trace()
    # Pollutants with limits
    for site in sep_sites:
        for pollutant in pollutants:
            if pollutant in limitsDF['Pollutant'].to_numpy():
                if limitsDF[limitsDF['Pollutant']==pollutant]['Averaging time [h]'].                to_numpy()[0] == 24:
                    df = twofourHourPoll
                    title = '24 hour average'
                elif limitsDF[limitsDF['Pollutant']==pollutant]['Averaging time [h]'].                to_numpy()[0] == 8:
                    df = eightHourPoll
                    title = '8 hour average'
                else:
                    df = oneHourPoll
                    title = '1 hour average'
            else:
                df = oneHourPoll
                title = '1 hour average'
        
            figLimits = plot_pollutant_multi_stations_date(start_date, end_date, pollutant,
                                                 df, site, limitsDF, title)
            figLimits.write_image('images/image'+str(i)+'.png')
            i+=1

    print('Done')
    pass

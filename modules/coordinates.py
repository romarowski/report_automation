import pandas as pd

coords_df = pd.DataFrame({'Primary Runway':[24.963136,46.712787], 
    'ATC Tower': [24.9560084,46.697312], 
    'Privet Aviation': [24.965448,46.722919], 
    'Air Cargo': [24.976318,46.694], 
    'Royal Terminal': [24.95376,46.695125], 
    'Secondary Runway 01': [24.956003,46.682273], 
    'Secondary Runway 02': [24.941005,46.691696], 
    'Fire Station': [24.963901,46.685287],
    'RIYADH FRONT(SASCO STATION 1)': [24.8448910438531,46.7326909415388],
    'SASCO Station 3': [24.8900915594346,46.693224316576],
    'Family Camp': [24.9415287040271,46.6493356990951],
    'AE123 Inbound K.S.R': [24.8549289506599,46.6816317072034],
    'CS 59 Storage': [24.9387025544531,46.7396476196533]}).transpose()

coords_df = coords_df.rename({0: 'lat', 1: 'lon'}, axis=1)
coords_df['Station']=coords_df.index
coords_df = coords_df[['Station', 'lat', 'lon']]

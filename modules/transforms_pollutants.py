import pandas as pd
import os 
import numpy as np

data = pd.read_csv('data/1h.csv')
data8 = pd.read_csv('data/8h.csv')
data24 = pd.read_csv('data/24h.csv')
limits = pd.read_csv('data/limits.csv')
runway_loc = pd.read_csv('data/location_runway.csv')
pollutant_name = []
pollutants = ['PM₂.₅ (µg/m³)', 'PM₁₀ (mg/m³)', 'PM₁ (µg/m³ )', 'CO₂ (ppm)', 
              'CO (mg/m³)', 'NO₂ (µg/m³ )', 'O₃ (µg/m³ )', 'H₂S (µg/m³ )',
              'NO (µg/m³ )', 'SO₂ (µg/m³)']
for pollutant in pollutants:
    pollutant_name.append(pollutant.split(' (', 1)[0])



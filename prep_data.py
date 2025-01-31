import pandas as pd
import requests
from typing import Dict, Optional
import os
def get_weather_data(lat: float, lon: float) -> Optional[Dict]:
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    
    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': 'metric' 
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def extract_weather_info(response: dict) -> dict:
    try:
        extracted_data = {
            'main_weather': response['weather'][0]['main'],
            'description': response['weather'][0]['description'],
            'weather_icon': response['weather'][0]['icon'],
            'weather_id': response['weather'][0]['id'],

            'timezone': response['timezone'],
            'timestamp': response['dt'],
            
            'latitude': response['coord']['lat'],
            'longitude': response['coord']['lon']
        }
        return extracted_data
        
    except (KeyError, TypeError, IndexError) as e:
        print(f"Error extracting weather data: {e}")
        return None
    
df = pd.read_csv('country-coord.csv')
df = df.dropna()
# Rename the columns to match the desired format
df = df.rename(columns={
    'Latitude (average)': 'LAT',
    'Longitude (average)': 'LONG',
})

df = df.reset_index(drop=True)

weather_main = []
weather_desc = []

for index, row in df.iterrows():
    lat = row['LAT']
    lon = row['LONG']
    
    res = get_weather_data(lat, lon)
    if res:
        weather_info = extract_weather_info(res)
        weather_main.append(weather_info['main_weather'])
        weather_desc.append(weather_info['description'])
    else:
        weather_main.append(None)
        weather_desc.append(None)
    
    if (index + 1) % 10 == 0:
        print(f"Processed {index + 1}/{len(df)} locations")

df['main_weather'] = weather_main
df['weather_description'] = weather_desc

df.to_csv('weather_data_with_conditions.csv', index=False)

print("\nFirst few rows of updated dataframe:")
print(df.head())
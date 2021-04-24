# -- coding: utf-8 --
"""
creates a sorted version of the weather data set with only the useful fields
"""

import pandas as pd
from datetime import datetime


# Datasets
weather_ds = pd.read_csv("../data/psamant/2017-2020_weather_data.csv")


#Inefficent algorithm that sorts through weather data set and adds it to new dependencies
def mysort(start, end):
    time = weather_ds.localhour[start]
    dt = datetime.strptime(time[:len(time)], '%Y-%m-%d %H:%M:%S')
    # creates dictionary for new pandas structure
    dependencies = {'Time': [time],
                    'Humidity': [weather_ds.humidity[start]],
                    'Temperature': [weather_ds.temperature[start]],
                    'Cloud_Cover': [weather_ds.cloud_cover[start]],
                    'Precip_Intensity': [weather_ds.precip_intensity[start]],
                    'Precip_Probablity': [weather_ds.precip_probability[start]]}
    for index in range(start+1, end):
        time = weather_ds.localhour[index]
        dt = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        i = 0
        while(1):
            if i >= len(dependencies['Time'])-1:
                dependencies['Time'].append(time)
                dependencies['Humidity'].append(weather_ds.humidity[index])
                dependencies['Temperature'].append(weather_ds.temperature[index])
                dependencies['Cloud_Cover'].append(weather_ds.cloud_cover[index])
                dependencies['Precip_Intensity'].append(weather_ds.precip_intensity[index])
                dependencies['Precip_Probablity'].append(weather_ds.precip_probability[index])
                break;
            compared = datetime.strptime(dependencies['Time'][i], '%Y-%m-%d %H:%M:%S')
            if dt < compared:
                dependencies['Time'].insert(i, time)
                dependencies['Humidity'].insert(i, weather_ds.humidity[index])
                dependencies['Temperature'].insert(i, weather_ds.temperature[index])
                dependencies['Cloud_Cover'].insert(i, weather_ds.cloud_cover[index])
                dependencies['Precip_Intensity'].insert(i, weather_ds.precip_intensity[index])
                dependencies['Precip_Probablity'].insert(i, weather_ds.precip_probability[index])
                break
            i += 1

    newDf = pd.DataFrame(dependencies)
    newDf.to_csv('newWeather.csv')

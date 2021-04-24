# -*- coding: utf-8 -*-

import pandas as pd
import json

data_path = '../data/psamant/2017-2020_weather_data.csv'

weather_ds = pd.read_csv(data_path)

longitude = {}
for index in range(0, len(weather_ds.latitude)):
     long = weather_ds.longitude[index]
     lat = weather_ds.latitude[index]
     timeString = weather_ds.localhour[index]
     latitude = {}
     info = {"timeStamp" : timeString,
             "tzOffSet": weather_ds.tz_offset[index],
             "summary": weather_ds.summary[index],
             "temperature": weather_ds.temperature[index],
             "dewPoint": weather_ds.dew_point[index],
             "humidity": weather_ds.humidity[index],
             "visibility": weather_ds.visibility[index],
             "apparent_temperature": weather_ds.apparent_temperature[index],
             "wind_speed": weather_ds.wind_speed[index],
             "cloud_cover": weather_ds.cloud_cover[index],
             "wind_bearing": weather_ds.wind_bearing[index],
             "pressure": weather_ds.pressure[index],
             "precip_intensity": weather_ds.precip_intensity[index],
             "precip_probability": weather_ds.precip_probability[index]}
     if long in longitude:
          if lat in latitude:
               latitude[lat].append[info]
          else:
               latitude[lat] = [info]
               longitude[long].append(latitude)
     else:
          if lat in latitude:
               latitude[lat].append[info]
          else:
               latitude[lat] = [info]
               longitude[long] = [latitude]

print("Dumping data....")

with open("weather_lat_lon.json", 'w') as f:
     json.dump(longitude, f)

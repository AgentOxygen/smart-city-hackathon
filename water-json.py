# -*- coding: utf-8 -*-

import pandas as pd
import json

data_path = '../data/psamant/water_final_data_hackathon.csv'

water_ds = pd.read_csv(data_path)

homes = {}
for index in range(0, len(water_ds.home_id)):
     hID = water_ds.home_id[index]
     timeString = water_ds.hourly_time[index]
     info = {"timeStamp" : timeString, "hourly_gal": water_ds.hourly_gal[index]}
     if hID in homes:
          homes[hID].append(info)
     else:
          homes[hID] = [info]

print("Dumping data....")

with open("weather_homes.json", 'w') as f:
     json.dump(homes, f)

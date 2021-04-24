# -*- coding: utf-8 -*-

import pandas as pd
import json

data_path = '../data/psamant/elec_final_data_hackathon.csv'

elec_ds = pd.read_csv(data_path)

homes = {}
for index in range(0, len(elec_ds.home_id)):
     hID = elec_ds.home_id[index]
     timeString = elec_ds.hourly_time[index]
     info = {"timeStamp" : timeString, "hConsumed": elec_ds.hourly_kwh[index], "hSolar": elec_ds.hourly_solar_kWh[index]}
     if hID in homes:
         homes[hID].append(info)
     else:
         print(hID)
         homes[hID] = [info]

print("Dumping data....")

with open("elec_homes.json", 'w') as f:
     json.dump(homes, f)

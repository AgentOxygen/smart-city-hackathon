import pandas as pd
import json
from datetime import datetime
from multiprocessing import Process

data_dir = "/home1/07644/oxygen/data/psamant/"


def get_datetime(timestamp):
    return datetime.strptime(timestamp[:len(timestamp) - 6], '%Y-%m-%d %H:%M')

def get_datetime_weather(timestamp):
    return datetime.strptime(timestamp[:len(timestamp) - 3], '%Y-%m-%d %H:%M')

def exec_run(start, finish):
    print("Loading index...")
    with open('combined.json', 'r') as f:
        data = json.load(f)
    
    print("Loading datasets...")
    o_elec_ds = pd.read_csv(data_dir + "elec_final_data_hackathon.csv")
    o_water_ds = pd.read_csv(data_dir + "water_final_data_hackathon.csv")
    o_weather_ds = pd.read_csv(data_dir + "2017-2020_weather_data.csv")
    
    data_w_dependencies = []
    
    print("Appending dependencies...")
    for index, pt in enumerate(data[start:finish]):
        weather_index = pt[0]
        humid = o_weather_ds[["humidity"]].values[weather_index].item()
        precip_intense = o_weather_ds[["precip_intensity"]].values[weather_index].item()
        cloud_cover = o_weather_ds[["cloud_cover"]].values[weather_index].item()
        precip_prob = o_weather_ds[["precip_probability"]].values[weather_index].item()
        temp = o_weather_ds[["temperature"]].values[weather_index].item()
        
        electricity_index = pt[1]
        hrly_kwh = o_elec_ds[["hourly_kwh"]].values[electricity_index].item()
        solar_kwh = o_elec_ds[["hourly_solar_kWh"]].values[electricity_index].item()
        ehome_id = o_elec_ds[["home_id"]].values[electricity_index].item()
        
        water_index = pt[2]
        hrly_gal = o_water_ds[["hourly_gal"]].values[water_index].item()
        whome_id = o_water_ds[["home_id"]].values[water_index].item()
        
        data_w_dependencies.append(((weather_index, humid, precip_intense, cloud_cover, precip_prob, temp), 
                                      (electricity_index, hrly_kwh, solar_kwh, ehome_id), 
                                      (water_index, hrly_gal, whome_id), 
                                      (pt[3]))) # Timestamp
    print("Outputting to JSON...")
    with open("dependencies_{}_to_{}.json".format(start, finish), 'w') as f:
        json.dump(data_w_dependencies, f, indent=2)
    print("Finished!")
        
for x in range(0, 100):
    Process(target=exec_run, args=(x*70,(x+1)*70,)).start()

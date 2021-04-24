import pandas as pd
import json
from datetime import datetime
from multiprocessing import Process
import threading

data_dir = "../data/psamant/"


def get_datetime(timestamp):
    return datetime.strptime(timestamp[:len(timestamp) - 6], '%Y-%m-%d %H:%M')

def get_datetime_weather(timestamp):
    return datetime.strptime(timestamp[:len(timestamp) - 3], '%Y-%m-%d %H:%M')

def exec_thread(start, finish):
    print("Loading datasets..")
    # Electricity Dataset
    o_elec_ds = pd.read_csv(data_dir + "elec_final_data_hackathon.csv")
    o_water_ds = pd.read_csv(data_dir + "water_final_data_hackathon.csv")
    
    
    print("Converting dataset timestamps to datetime objects..")
    elec_ds = [(index, get_datetime(i.item())) for index, i in enumerate(o_elec_ds[["hourly_time"]].values[start:finish])]
    water_ds = [(index, get_datetime(i.item())) for index, i in enumerate(o_water_ds[["hourly_time"]].values[start:finish])]
    
    
    print("Cross checking datetime objects for commonalities..")
    common = []
    for elec_index_ts in elec_ds:
        for water_index_ts in water_ds:
            if elec_index_ts[1] == water_index_ts[1]:
                common.append((elec_index_ts[0], water_index_ts[0], elec_index_ts[1]))
    
    print("Listing home IDs..")
    elec_ds = [i for i in o_elec_ds[["home_id"]].values[:10000]]
    water_ds = [i for i in o_water_ds[["home_id"]].values[:10000]]
    
    common_home = []
    for common_ei_wi_ts in common:
        if elec_ds[common_ei_wi_ts[0]] == water_ds[common_ei_wi_ts[1]]:
            common_home.append(common_ei_wi_ts)
    
    print("Loading weather dataset..")
    o_weather_ds = pd.read_csv(data_dir + "2017-2020_weather_data.csv")
    print("Converting weather dataset timestamps to datetime objects..")
    weather_ds = [(index, get_datetime_weather(i.item())) for index, i in enumerate(o_weather_ds[["localhour"]].values[start:finish])]
    
    weather_common = []
    print("Cross checking weather datatimes and converting to integer timestamps and JSON serializable lists..")
    for common_ei_wi_ts in common_home:
        for weather_index_ts in weather_ds:
            if weather_index_ts[1] == common_ei_wi_ts[2]:
                weather_common.append((weather_index_ts[0], common_ei_wi_ts[0], common_ei_wi_ts[1], common_ei_wi_ts[2].timestamp()))
    
    print("Outputting to JSON..")
    with open("sorted_datapairs/commonalities_{}_to_{}.json".format(start, finish), 'w') as f:
        # Outputs list of tupes containing info: (weather index, electricity index, water index, timestamp)
        # Use datetime.fromtimestamp() to convert back to datetime object
        json.dump(weather_common, f, indent=2)
    print("Finished!")

for x in range(0, 109):
    Process(target=exec_thread, args=(x*10000,(x+1)*10000,)).start()

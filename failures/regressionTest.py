# -*- coding: utf-8 -*-


import numpy as np
import json
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

with open('C:/Users/willc/Downloads/combined-dep.json', 'r') as f:
    data = json.load(f)

train_x = {'Time' : [],
          'Humid' : [],
          'Precip_Intense' : [],
          'Cloud_Cover' : [],
          'Precip_Prob' : [],
          'Temperature' : [],
          'Hrly_Kwh' : [],
          'Solar_Kwh' : [],
          'Ehome_Id' : [],
          'Whome_Id' : []}
test_x = {'Time' : [],
          'Humid' : [],
          'Precip_Intense' : [],
          'Cloud_Cover' : [],
          'Precip_Prob' : [],
          'Temperature' : [],
          'Hrly_Kwh' : [],
          'Solar_Kwh' : [],
          'Ehome_Id' : [],
          'Whome_Id' : []}
train_y = {'Hrly_Gal' : []}
test_y = {'Hrly_Gal' : []}
for index in range(0, len(data)):
    ((weather_index, humid, precip_intense, cloud_cover, precip_prob, temp),
     (electricity_index, hrly_kwh, solar_kwh, ehome_id),
     (water_index, hrly_gal, whome_id),
     (timestamp)) = data[index]
    dt = datetime.fromtimestamp(timestamp)
    day = dt - datetime(2017, 1, 1, 0, 0)
    if(dt < datetime(2018, 1, 1, 0, 0)):
        train_x['Time'].append(day.days)
        train_x['Humid'].append(humid)
        train_x['Precip_Intense'].append(precip_intense)
        train_x['Cloud_Cover'].append(cloud_cover)
        train_x['Precip_Prob'].append(precip_prob)
        train_x['Temperature'].append(temp)
        train_x['Hrly_Kwh'].append(hrly_kwh)
        train_x['Solar_Kwh'].append(solar_kwh)
        train_x['Ehome_Id'].append(ehome_id)
        train_x['Whome_Id'].append(whome_id)
        train_y['Hrly_Gal'].append(hrly_gal)
    else:
        test_x['Time'].append(day.days)
        test_x['Humid'].append(humid)
        test_x['Precip_Intense'].append(precip_intense)
        test_x['Cloud_Cover'].append(cloud_cover)
        test_x['Precip_Prob'].append(precip_prob)
        test_x['Temperature'].append(temp)
        test_x['Hrly_Kwh'].append(hrly_kwh)
        test_x['Solar_Kwh'].append(solar_kwh)
        test_x['Ehome_Id'].append(ehome_id)
        test_x['Whome_Id'].append(whome_id)
        test_y['Hrly_Gal'].append(hrly_gal)


trainX = pd.DataFrame(train_x)
testX = pd.DataFrame(test_x)

trainY = pd.DataFrame(train_y)
testY = pd.DataFrame(test_y)

regression = LinearRegression()
regression.fit(trainX, trainY)
y_pred = regression.predict(testX)


mae = mean_absolute_error(testY, y_pred)
mse = mean_squared_error(testY, y_pred)
rmse = np.sqrt(mse)

plt.scatter(trainX['Time'],trainY, color='black')
plt.scatter(testX['Time'],testY, color='blue')
plt.scatter(testX['Time'],y_pred, color='red')
plt.xlabel("Days from 2017/01/01")
plt.ylabel("Water Consumption (gal)")
plt.xticks(np.arange(0,1360, step=360))
plt.yticks()
plt.text(600,420, "mean absoulute error: " + str(mae))
plt.text(600,400, "mean squared error: " + str(mae))

plt.show()
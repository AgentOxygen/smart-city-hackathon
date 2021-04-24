import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

data_dir = "C:/Users/Camer/Documents/Smart City Hackathon/data/"

# Electricity Dataset
elec_ds = pd.read_csv(data_dir + "elec_final_data_hackathon.csv")

# hourly_kwh
# hourly_time

dt = 8000

# Create linear regression object
regr = linear_model.LinearRegression()

# Get hourly timestamp and convert to datetime object
datetime_values = []#elec_ds.hourly_time[:20] * 0

for index in range(0, dt):
    time = elec_ds.hourly_time[index]
    datetime_values.append(datetime.strptime(time[:len(time) - 6], '%Y-%m-%d %H:%M'))

# Get time from first timestamp
t0 = datetime_values[0]
time_values = []# = elec_ds.hourly_kwh[:20] * 0
for index, time in enumerate(datetime_values[1:]):
    time_since_origin = (datetime_values[index] - t0).seconds / (60*60) + (datetime_values[index] - t0).days * 24
    time_values.append([time_since_origin, elec_ds.hourly_solar_kWh[index]])

y = []
for index in range(0, dt - 1):
    y.append(elec_ds.hourly_kwh[index])

print("start:" + str(datetime_values[0]))
print("end:" + str(datetime_values[dt - 1]))
print("Time frame: {}".format(datetime_values[dt - 1] - datetime_values[0]))

X = np.array(time_values)

regr.fit(X, y)

prediction = regr.predict(X)
plt.title("Time and Solar affects Consumption")
plt.scatter(X, y,  color='black', s=10)
plt.plot(X, prediction, color='blue', linewidth=3)

plt.show()
plt.savefig("output.png")

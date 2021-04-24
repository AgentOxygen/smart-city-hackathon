import numpy as np
import random
from sklearn.metrics import mean_squared_error, r2_score
import json
import conor_polyreg


# CAMERONS SCRIPT GOES HERE TO GET X AND Y DATA
data_dir = "sorted_datapairs/"

with open(data_dir + 'combined-dep.json', 'r')as f:
    data = json.load(f)

x = []
y = []

for data_pt in data:
    ((weather_index, humid, precip_intense, cloud_cover, precip_prob, temp), 
                                          (electricity_index, hrly_kwh, solar_kwh, ehome_id), 
                                          (water_index, hrly_gal, whome_id), 
                                          (timestamp)) = data_pt
    x.append(hrly_kwh)
    y.append(hrly_gal)



# FIT DATA WITH REGRESSION

# order polynomial that we choose to evaluate the data as
order = 5

# call polynomial regressor
c = conor_polyreg.polyreg(x,y,order)

# solved function (order needs to match the variable "order")
f = lambda v : c[0] + c[1]*(v) + c[2]*(v**2) + c[3]*(v**3) + c[4]*(v**4) + c[5]*(v**5) 

# predicted y data
y_pred = f(x)



# ACCURACY TESTS

# mean squared error (0 is perfect prediction)
print('Mean Squared Error: %.2f' % mean_squared_error(y,y_pred))

# coefficient of determination (1 is perfect prediction)
print('Coefficient of Determination: %.2f' % r2_score(y,y_pred))

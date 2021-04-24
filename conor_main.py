import numpy as np
import random
import json
from sklearn.metrics import r2_score
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


# test data -- f(x) = 1 - x + x^2 + 5x^3
x_test = np.array([-2,-1,0,1,2])
y_test = np.array([-33,-2,1,6,43])


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

# coefficient of determination (1 is perfect)
print('Coefficient of Determination: %.2f' % r2_score(y,y_pred))

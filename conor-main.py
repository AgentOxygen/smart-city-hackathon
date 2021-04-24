from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score
import numpy as np
import random
import json


# read in json data files
with open('elec_homes.json') as f1:
    data_elec = json.load(f1)

with open('water_homes.json') as f2:
    data_water = json.load(f2)


# choose a house
NUM_OF_HOMES = len(data_water)
hID = random.randint(1,NUM_OF_HOMES)
home_count = 1
for home in data_water: # could also use data_elec, it shouldn't matter
    if home_count == hID:
        hID = home
        break
    home_count += 1


# load the proper x-y data into data arrays


# make data arrays
y = []
x = []

for i in range(len(data_water[hID])):
    
    # water consumption
    y.append(data_water[hID][i]['hourly_gal'])
    
    # power consumption
    x.append(data_elec[hID][i]['hConsumed'])


# regression


# polynomial regression as a 5th order polynomial
model = Pipeline([('poly', PolynomialFeatures(degree=5)), ('linear', LinearRegression(fit_intercept=False))])
model = model.fit(x, y)
coefficients = model.named_steps['linear'].coef_

# solved function
f = lambda v : coefficients[0] + (v)*coefficients[1] + (v**2)*coefficients[2] + (v**3)*coefficients[3] + (v**4)*coefficients[4] + (v**5)*coefficients[5] 

# solved y data
y_solved = f(x)


# accuracy test


# coefficient of determination (1 is perfect prediction)
print('Coefficient of Determination: %.2f' % r2_score(y,y_solved))

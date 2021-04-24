# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 18:08:35 2021

@authors: Conor Donihoo, Cameron Cummins, Will Chin
"""

import numpy as np
import scipy
import json
from sklearn.metrics import r2_score

def polyreg(x,y,order):

    # We have an error function S(a0,a1,...,a_order) where "order" is the
    # degree of the polynomial that best describes the data being passed
    # into the lsPolynomial function.
    
    # A polynomial is in the form y = a0 + a1*x + ... + a_order*x^order
    
    # Therefore, S(a) = sum( (y - (a0 + a1*x + ... + a_order*x^order) )^2 )
    
    # We can turn this into a linear system of equations by taking the
    # gradient of the error function S. We can then construct the
    # constant matrix "A" and the RHS vector "b" to solve for the solution
    # vector "a". 
    
    # A = [ c0 c1 c2 . . . cOrder ]   Where ci = sum( x^i )
    #     [ c1 c2 . . .     .  .  ]          
    #     [ c2 .  . .    .     .  ]            and
    #     [ .  .  .   .        .  ]   
    #     [ .  .  .      .     .  ]   b = [b0 b1 ... bOrder]'
    #     [ .  .            .  .  ]
    #     [ cOrder . . . cOrder*2 ]   Where bi = sum( y * x^i )
    
    # We can rewrite A as:
    # A = [ cOrder . . . c2 c1 c0 ]
    #     [ .   .     . . . c2 c1 ]          
    #     [ .      .     . . . c2 ]
    #     [ .         .        .  ]   
    #     [ .      .     .     .  ]
    #     [ .   .           .  .  ]
    #     [ cOrder*2 . . . cOrder ]

    # convert data arrays to numpy arrays
    x = np.array(x)
    y = np.array(y)

    # create constant matrix "A" and RHS vector "b"
    A = np.zeros((order+1,order+1))
    b = np.zeros(order+1)

    # place  values in the matrix
    aSize = 0 # size of the array being put onto the diagonal
    for n in range(order*2+1):
        if n <= order:
            aSize = aSize+1
            A[np.arange(n+1),np.arange(order-n,order+1)] = np.diag(np.ones((1,aSize))*sum(x**n))
        else:
            aSize = aSize-1
            A[np.arange(n-order,order+1),np.arange(2*order-n+1)] = np.diag(np.ones((1,aSize))*sum(x**n))


    # place values in the vector
    for n in range(order+1):
        b[n] = sum(y*(x**n))


    # solve for coefficient vector "a" in the form [a0 a1 a2 ... aOrder]
    a = np.linalg.solve(A,b)
    a = a[::-1]
    
    # return coefficient vector "a"
    return a

data_dir = ""

with open(data_dir + 'combined-dep.json', 'r')as f:
    data = json.load(f)

x = []
y = []

# Pull data from JSON
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
c = polyreg(x,y,order)

# solved function (order needs to match the variable "order")
f = lambda v : c[0] + c[1]*(v) + c[2]*(v**2) + c[3]*(v**3) + c[4]*(v**4) + c[5]*(v**5) 

# predicted y data
y_pred = f(np.array(x))


# ACCURACY TESTS

# coefficient of determination (1 is perfect)
print('Coefficient of Determination: %.2f' % r2_score(y,y_pred))
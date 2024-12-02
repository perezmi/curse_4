#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 14:03:38 2024

@author: verz
"""

import numpy as np

def get_circle_coord(R, digits,x0,y0,start_fi):
    X=[]
    Y=[]
    for fi in np.arange(start_fi,2*np.pi+start_fi,2*np.pi/digits):
        X.append(x0+R*np.cos(fi));
        Y.append(y0+R*np.sin(fi));
    X.append(X[0])
    Y.append(Y[0])
    return np.array([X,Y]).transpose()
def arctan_mod(dX,dY):
    psi=np.arctan(dY/dX)
    if(dX<0):
        psi=psi+np.pi
    return psi
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 22:40:28 2024

@author: verz
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

RIT=pd.DataFrame()
RIT["R"]=np.array([10,25,50,100,200])
RIT["Ih"]=np.array([166,173,176,178,179])
CIT=pd.DataFrame()
CIT["C"]=np.array([0,5,10,15,20])
CIT["Ih"]=np.array([6.41,91.4,149,178,193])
RTNC=pd.DataFrame()
RTNC["R"]=np.array([10,25,50,100,200])
RTNC["Ih"]=np.array([220,220,220,220,220])
CTNC=pd.DataFrame()
CTNC["C"]=np.array([0,5,10,15,20])
CTNC["Ih"]=np.array([220,220,220,220,220])

plt.figure(figsize=[21, 30])
plt.subplot(2,1,1)
plt.plot(RIT["R"],RIT["Ih"])
plt.plot(RTNC["R"],RTNC["Ih"])
plt.legend(["сеть IT","сеть TN-C"])
plt.xlabel("Rh, кОм")
plt.ylabel("Ih, мА")
plt.title("Зависимость Ih(R)")
plt.grid(True)

plt.subplot(2,1,2)
plt.plot(CIT["C"],CIT["Ih"])
plt.plot(CTNC["C"],CTNC["Ih"])
plt.xlabel("C, мкФ")
plt.ylabel("Ih, мА")
plt.legend(["сеть IT","сеть TN-C"])
plt.title("Зависимость Ih(C)")
plt.grid(True)
plt.savefig("Зависимости Ih(R), Ih(C)")

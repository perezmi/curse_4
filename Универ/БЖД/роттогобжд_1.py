#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 21:49:19 2024

@author: verz
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
tabl3=pd.DataFrame()
tabl3["lgf"]=np.array([1.7,2.0,2.7,3.0,3.7])
tabl3["Ih"]=np.array([9.7,10,11,14,50])*0.001
U=40
plt.figure()
tabl3["Zh"]=U/tabl3["Ih"]

plt.figure(figsize=[21, 30])
plt.subplot(2,1,1)
plt.plot(tabl3["lgf"],tabl3["Zh"])
plt.grid(True)
plt.xlabel("Частота тока\nlg(f)")
plt.ylabel("Сопротивление тела человека Zh,Ом")
plt.title("Зависимость сопротивления человека\nот частоты приложенного тока")
tabl4=pd.DataFrame()
tabl4["Uh"]=np.arange(0,230,10)+4
tabl4["Uh"][len(tabl4["Uh"])]=220

plt.subplot(2,1,2)
tabl4["Ih"]=np.array([0.9,3.4,5.9,7.9,11,15,20,26,33,40,47,56,64,73,81,90,99,108,116,124,132,139,143])*0.001
tabl4["Zh"]=tabl4["Uh"]/tabl4["Ih"]
plt.plot(tabl4["Uh"],tabl4["Zh"])
plt.grid(True)
plt.xlabel("Приложенное напряжение Uh, В")
plt.ylabel("Сопротивление тела человека Zh,Ом")
plt.title("Зависимость сопротивления человека\nот величины приложенного напряжения")
plt.savefig("Зависимость сопротивления человека от величины приложенного напряжения")
print(tabl3)
print(tabl4)
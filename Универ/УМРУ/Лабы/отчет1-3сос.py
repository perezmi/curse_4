#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 09:25:01 2024

@author: verz
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
mod="lab3"
file_in_id=mod+"_pereverzev_12e.txt"
file_in_exp=mod+"_pereverzev_12e_out.txt"
file_df=mod+"_pereverzev_12e_df.txt"
dt=0.05
a=0.05
b=1/dt*0.05

def jdtfp(df,xlabel,ylabel,data,name):
    plt.figure(figsize=[8.3,5])
    for dat in data:
        plt.plot(df[dat[0]],df[dat[1]],label=dat[2])
    plt.grid(True)
    plt.legend()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(name)
    plt.savefig(mod+"_"+name+".png")
    plt.title(name)
   # plt.show()
    plt.close()
def integra_XYPsi(Vt,Vl,Om):
    X=np.zeros_like(Vt)
    Y=np.zeros_like(Vl)
    Psi=np.zeros_like(Om)
    for i in np.arange(1,len(Vt)):
        X[i]=X[i-1]+dt*(Vt[i]*np.cos(Psi[i-1])-Vl[i]*np.sin(Psi[i-1]))
        Y[i]=Y[i-1]+dt*(Vl[i]*np.cos(Psi[i-1])+Vt[i]*np.sin(Psi[i-1]))
        Psi[i]=Psi[i-1]+Om[i]*dt
        
    return np.array([X,Y,Psi])
def square_err(E):
    err=0
    for e in E: 
        err=err+e**2
    err=err**0.5/len(E)
    return err
def tlom2xyom(df,Vt,Vl,Om):
    Vx=np.zeros_like(df[Vt])
    Vy=np.zeros_like(df[Vl])
    Psi=0
    for i in np.arange(df[Vt].size):
        [Vx[i],Vy[i]]=np.matmul(turn(Psi),np.array([df[Vt][i],df[Vl][i],df[Om][i]]))[:2]
        Psi=Psi+df[Om][i]*dt
    return [Vx,Vy]
def f2df():
    [V_Tid,V_Lid,Omid]=np.genfromtxt(file_in_id).T
    [V_Texp,V_Lexp,Omexp]=np.genfromtxt(file_in_exp).T[9:12,1:]
    [Xid,Yid,Psiid]=integra_XYPsi(V_Tid, V_Lid, Omid)
    [Xexp,Yexp,Psiexp]=integra_XYPsi(V_Texp, V_Lexp, Omexp)    
    df = pd.DataFrame(np.array([V_Tid,V_Lid,Omid,Xid,Yid,Psiid,V_Texp,V_Lexp,Omexp,Xexp,Yexp,Psiexp]).T
                      ,columns=["V_Tid","V_Lid","Omid","Xid","Yid","Psiid","V_Texp","V_Lexp","Omexp","Xexp","Yexp","Psiexp"])
    return df
def simple_d(A):
    B=np.zeros_like(A)
    for i in np.arange(1,A.size):
        B[i]=(A[i]-A[i-1])/dt
    return B
def add_err(df,Vexp,Vid,head):
    err=pd.DataFrame(df[Vexp]-df[Vid],columns=[head]) #exp-id
    df[head]=err
    
def add_parasite(df,V,head):
    parasite=np.zeros_like(df[V])
    for i in np.arange(1, df[V].size):
        parasite[i]=(df[V][i]-df[V][i-1])/dt
    df[head]=parasite
    
def turn(Psi):
    return np.array([[np.cos(Psi),-np.sin(Psi),0],
                     [np.sin(Psi),np.cos(Psi),0],
                     [0,0,1]])

def feedback(Vid,Xid,Verr,pf=""):
    Vreal=np.zeros_like(Vid)
    Xreal=np.zeros_like(Xid)
    Vupr=np.zeros_like(Vid)
    Vdop=np.zeros_like(Vid)
    for i in np.arange(Vupr.shape[1]):
        Vreal[:,i]=Vupr[:,i-1]+Verr[:,i]*dt
        Xreal[:,i]=Xreal[:,i-1]+dt*np.matmul(turn(Xreal[2,i-1]),Vreal[:,i])
        Vupr[:,i]=Vid[:,i]+a*(Vid[:,i]-Vreal[:,i])+b*np.matmul(turn(-Xreal[2,i-1]),
                                                               Xid[:,i]-Xreal[:,i])
        Vdop[:,i]=np.matmul(turn(Xreal[2,i]),Vreal[:,i])
    [df["V_Treal"],df["V_Lreal"],df["Omreal"]]=Vreal
    [df["Xreal"],df["Yreal"],df["Psireal"]]=Xreal
    [df["V_Tupr"],df["V_Lupr"],df["Omupr"]]=Vupr
    [df["Xupr"+pf],df["Yupr"+pf],df["Psiupr"+pf]]=integra_XYPsi(Vupr[0],Vupr[1],Vupr[2])

df=f2df()
add_err(df, "V_Lexp", "V_Lid", "V_Lerr")
add_err(df, "V_Texp", "V_Tid", "V_Terr")
add_err(df, "Omexp", "Omid", "Omerr")
add_parasite(df, "V_Lerr", "V_Lpar")
add_parasite(df, "V_Terr", "V_Tpar")
add_parasite(df, "Omerr", "Ompar")
feedback(np.array([df["V_Tid"],df["V_Lid"],df["Omid"]]),
             np.array([df["Xid"],  df["Yid"],df["Psiid"]]),
             np.array([df["V_Tpar"],df["V_Lpar"],df["Ompar"]]))

jdtfp(df,"X","Y",[["Xid","Yid","ideal"],
                 ["Xexp","Yexp","exp"],
                 ["Xreal","Yreal","real"],
                 ["Xupr","Yupr","upr"]]
      , "Координаты")
df["t"]=np.arange(df["Xid"].size)*dt

jdtfp(df, "t, с", "X", [["t","Xid","ideal"],
                           ["t","Xexp","exp"],
                           ["t","Xreal","real"],
                           ["t","Xupr","upr"]], "Xega")
jdtfp(df, "t, с", "Y", [["t","Yid","ideal"],
                           ["t","Yexp","exp"],
                           ["t","Yreal","real"],
                           ["t","Yupr","upr"]], "Yega")
jdtfp(df, "t, с", "Psi", [["t","Psiid","ideal"],
                           ["t","Psiexp","exp"],
                           ["t","Psireal","real"],
                           ["t","Psiupr","upr"]], "Psiega")
jdtfp(df, "t, с", "V_T", [["t","V_Tid","ideal"],
                           ["t","V_Texp","exp"],
                           ["t","V_Treal","real"],
                           ["t","V_Tupr","upr"]], "V_T")
jdtfp(df, "t, с", "V_L", [["t","V_Lid","ideal"],
                           ["t","V_Lexp","exp"],
                           ["t","V_Lreal","real"],
                           ["t","V_Lupr","upr"]], "V_L")
jdtfp(df, "t, с", "Om", [["t","Omid","ideal"],
                           ["t","Omexp","exp"],
                           ["t","Omreal","real"],
                           ["t","Omupr","upr"]], "Omega")
df["Vxid"]=simple_d(df["Xid"])
df["Vyid"]=simple_d(df["Yid"])
df["Vxexp"]=simple_d(df["Xexp"])
df["Vyexp"]=simple_d(df["Yexp"])
df["Vxreal"]=simple_d(df["Xreal"])
df["Vyreal"]=simple_d(df["Yreal"])
df["Vxupr"]=simple_d(df["Xupr"])
df["Vyupr"]=simple_d(df["Yupr"])

jdtfp(df, "t, с", "Vx", [["t","Vxid","ideal"],
                           ["t","Vxexp","exp"],
                           ["t","Vxreal","real"],
                           ["t","Vxupr","upr"]],"Vx")
jdtfp(df, "t, с", "Vy", [["t","Vyid","ideal"],
                           ["t","Vyexp","exp"],
                           ["t","Vyreal","real"],
                           ["t","Vyupr","upr"]], "Vy")


jdtfp(df, "t, с", "Om", [["t","Omid","ideal"],
                           ["t","Omexp","exp"],
                           ["t","Omreal","real"],
                           ["t","Omupr","upr"]], "Om")
with open(mod+'_err.md', 'w') as f:
    for l in ["Отклонение идеальной траектории от экспериментальной по оси X: ", str(format(square_err(df["Xid"]-df["Xexp"]),'.6f')),"м\n",
          "Отклонение идеальной траектории от скорректированной по оси X: ", str(format(square_err(df["Xid"]-df["Xreal"]),'.6f')),"м\n",
          "Отклонение идеальной траектории от экспериментальной по оси Y: ", str(format(square_err(df["Yid"]-df["Yexp"]),'.6f')),"м\n",
          "Отклонение идеальной траектории от скорректированной по оси Y: ", str(format(square_err(df["Yid"]-df["Yreal"]),'.6f')),"м\n",
          "Отклонение идеальной траектории от экспериментальной по углу поворота $\Psi$: ", str(format(square_err(df["Psiid"]-df["Psiexp"]),'.6f')),"рад\n"
          "Отклонение идеальной траектории от скорректированной по углу поворота $\Psi$: ", str(format(square_err(df["Psiid"]-df["Psireal"]),'.6f')),"рад\n",
          "Отклонение идеальной $V_T$ от экспериментальной: ", str(format(square_err(df["V_Tid"]-df["V_Texp"]),'.6f')),"м/с\n",
          "Отклонение идеальной $V_T$ от скорректированной: ", str(format(square_err(df["V_Tid"]-df["V_Treal"]),'.6f')),"м/с\n",
          "Отклонение идеальной $V_L$ от экспериментальной: ", str(format(square_err(df["V_Lid"]-df["V_Lexp"]),'.6f')),"м/с\n",
          "Отклонение идеальной $V_L$ от скорректированной: ", str(format(square_err(df["V_Lid"]-df["V_Lreal"]),'.6f')),"м/с\n",
          "Отклонение идеальной $\omega$ от экспериментальной: ", str(format(square_err(df["Omid"]-df["Omexp"]),'.6f')),"рад/с\n"
          "Отклонение идеальной $\omega$ от скорректированной: ", str(format(square_err(df["Omid"]-df["Omreal"]),'.6f')),"рад/с\n"
          ]:    
        f.write(l)

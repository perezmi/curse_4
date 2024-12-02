#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 16:17:14 2024

@author: verz
"""

import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import numpy.linalg as la
d1=0.5
phi2=np.pi/180*60;
phi3=np.pi/180*30;
d4=1
l2=1.5
U=np.array([0.5,-1.2,0])
def K(k,d4=1):
    return np.diag([1,1/np.sqrt(k**2*l2**2+d4**2),1/d4,1])

J=np.array([[0,-l2*np.sin(phi2)-d4*np.sin(phi2+phi3),-d4*np.sin(phi2+phi3),np.cos(phi2+phi3)],
            [1,l2*np.cos(phi2)+d4*np.cos(phi2+phi3),d4*np.cos(phi2+phi3),np.sin(phi2+phi3)],
            [0,1,1,0]])

Jz=np.matmul(J,K(1))
"""
#2.1.1 Pinv
dqPinv=K(1)@np.linalg.pinv(Jz)@U
#2.1.2 SVD
[U1,S1,V1]=np.linalg.svd(Jz,full_matrices=False)
dqSVD=K(1)@V1.T@np.linalg.inv(np.diag(S1))@U1.T@U
#2.1.3 Jzp
Jzp=Jz.T@np.linalg.inv(Jz@Jz.T)
dqJzp=K(1)@Jzp@U
#2.1.4 QR
[Q,R]=sp.linalg.qr(Jz.T,mode="economic")
dqQR=K(1)@Q@np.linalg.inv(R.T)@U
#2.1.5
alpha = 0.0001
dqRound1 = K(1)@Jz.T@sp.linalg.inv(Jz@Jz.T+alpha**2 * np.eye(3))@U
dqRound2 = K(1)@sp.linalg.inv(Jz.T@Jz+alpha**2 * np.eye(4))@Jz.T@U

df1=pd.DataFrame()
df1["Pinv"]=[0,0,0,0,0]
df1["Pinv"][:4]=dqPinv-dqPinv
df1["Pinv"][4]=np.linalg.norm(J@dqPinv-U)
df1["SVD"]=[0,0,0,0,0]
df1["SVD"][:4]=dqPinv-dqSVD
df1["SVD"][4]=np.linalg.norm(J@dqSVD-U)
df1["JZP"]=[0,0,0,0,0]
df1["JZP"][:4]=dqPinv-dqJzp
df1["JZP"][4]=np.linalg.norm(J@dqJzp-U)
df1["QR"]=[0,0,0,0,0]
df1["QR"][:4]=dqPinv-dqQR
df1["QR"][4]=np.linalg.norm(J@dqQR-U)
df1["R1"]=[0,0,0,0,0]
df1["R1"][:4]=dqPinv-dqRound1
df1["R1"][4]=np.linalg.norm(J@dqRound1-U)
df1["R2"]=[0,0,0,0,0]
df1["R2"][:4]=dqPinv-dqRound2
df1["R2"][4]=np.linalg.norm(J@dqRound2-U)
df2=pd.DataFrame()

for k in [1,10,100]:
    Jz=J@K(k)    
    
    [Q,R]=sp.linalg.qr(Jz.T,mode="economic")
    dqQR1=K(k)@Q@np.linalg.inv(R.T)@U
    print(dqQR1)
    df2[k]=dqQR1
print(df2)
"""
R=1.6
Om=0.15
dt=0.006
d1=0.5
phi2=np.pi/180*60;
phi3=np.pi/180*30;
d4=1
df3=pd.DataFrame()
df3["t"]=np.arange(0,3*np.pi/2/Om,dt)
df3["x"]=l2*np.cos(phi2)+d4*np.cos(phi2+phi3)+R*(1-np.cos(Om*df3["t"]))
df3["y"]=d1+l2*np.sin(phi2)+d4*np.sin(phi2+phi3)-R*np.sin(Om*df3["t"])
df3["psi"]=phi2+phi3

plt.figure()
plt.plot(df3["x"],df3["y"])
plt.grid(True)
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Траектория движения точки А")
plt.savefig("Траектория движения точки А"+".png")
plt.show()
plt.close()

plt.figure()
plt.plot(df3["t"],df3["x"])
plt.grid(True)
plt.xlabel("xA")
plt.ylabel("t")
plt.title("xA(t)")
plt.savefig("xA(t)"+".png")
plt.show()
plt.close()

plt.figure()
plt.plot(df3["t"],df3["y"])
plt.grid(True)
plt.xlabel("yA")
plt.ylabel("t")
plt.title("yA(t)")
plt.savefig("yA(t)"+".png")
plt.show()
plt.close()

def simple_d(A):
    B=np.zeros_like(A)
    for i in np.arange(1,A.size):
        B[i]=(A[i]-A[i-1])/dt
    return B
df3["vx"]=simple_d(df3["x"])#R*np.sin(Om*df3["t"])
df3["vy"]=simple_d(df3["y"])#-R*np.cos(Om*df3["t"])
df3["om"]=simple_d(df3["psi"])

df3["d1"]=np.zeros_like(df3["t"])
df3["phi2"]=np.zeros_like(df3["t"])
df3["phi3"]=np.zeros_like(df3["t"])
df3["d4"]=np.zeros_like(df3["t"])
df3["cond"]=np.zeros_like(df3["t"])
#df3["sing2"]=np.zeros_like(df3["t"])
#df3["sing1"]=np.zeros_like(df3["t"])

df3["d1"][0]=d1
df3["phi2"][0]=phi2
df3["phi3"][0]=phi3
df3["d4"][0]=d4
k=1
for i in np.arange(1,len(df3["t"])):
    U=np.array([df3["vx"][i],
                df3["vy"][i],
                df3["om"][i]])
    d1=df3["d1"][i-1]
    phi2=df3["phi2"][i-1]
    phi3=df3["phi3"][i-1]
    d4=df3["d4"][i-1]
    J=np.array([[0,-l2*np.sin(phi2)-d4*np.sin(phi2+phi3),   -d4*np.sin(phi2+phi3),    np.cos(phi2+phi3)],
                [1,l2*np.cos(phi2)+d4*np.cos(phi2+phi3),     d4*np.cos(phi2+phi3),     np.sin(phi2+phi3)],
                [0,1,1,0]])
    Jz=J@K(k,d4)
    df3["cond"][i]=np.linalg.cond(Jz)
    #df3["sing1"][i]=la.det(Jz@Jz.T)
    #df3["sing2"][i]=la.det(J@J.T)
    Jzp=Jz.T@np.linalg.inv(Jz@Jz.T)
    dq=K(k,d4)@Jzp@U
    #dq=K(k)@np.linalg.pinv(Jz)@U
    print(i/len(df3["t"])*100,"%")
    #alpha = 0.05
    #dq = K(1)@Jz.T@sp.linalg.inv(Jz@Jz.T+alpha**2 * np.eye(3))@U
    [df3["d1"][i],df3["phi2"][i],df3["phi3"][i],df3["d4"][i]]=[d1,phi2,phi3,d4]+dq*dt

#находим моменты, когда конфигурация сингулярна
singt=[]
for i in np.arange(df3["t"].shape[0]):
    if df3["cond"][i]>10000: singt.append(i)
#графики
for name in np.array(df3.columns):
    if name!="t":
        plt.figure()
        plt.plot(df3["t"],df3[name])
        #plt.plot(df3["t",singt],df3[name,singt],"*")
        plt.grid(True)
        plt.xlabel(name)
        plt.ylabel("t")
        plt.title(name+"(t)")
        plt.savefig(name+"(t)"+".png")
        plt.show()
        plt.close()
XA=np.zeros_like(df3["t"])
YA=np.zeros_like(df3["t"])
Psi=np.zeros_like(df3["t"])
for i in np.arange(len(df3["t"])):
    d1=df3["d1"][i]
    phi2=df3["phi2"][i]
    phi3=df3["phi3"][i]
    d4=df3["d4"][i]
    XA[i]=l2*np.cos(phi2)+d4*np.cos(phi2+phi3)
    YA[i]=d1+l2*np.sin(phi2)+d4*np.sin(phi2+phi3)
plt.figure()

plt.plot(df3["x"],df3["y"])
plt.plot(XA,YA)
#plt.plot(XA[singt],YA[singt],"*")
plt.grid(True)

def mani_draw(df,t):
    d1=df["d1",t]
    phi2=df["phi2",t]
    phi3=df["phi3",t]
    d4=df["d4",t]
    x=[0]
    y=[0]
    x.append(0)
    y.append(d1)
    x.append(l2*np.cos(phi2))
    y.append(d1+l2*np.sin(phi2))
    x.append(l2*np.cos(phi2)+d4*np.cos(phi2+phi3))
    y.append(d1+l2*np.sin(phi2)+d4*np.sin(phi2+phi3))
    
    plt.plot(x,y)

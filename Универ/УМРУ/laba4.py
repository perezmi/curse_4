import numpy as np
V=0.3*2*np.pi/30
O=2*np.pi/10
t=np.arange(0,30,0.05)
Vx=-V*np.sin(2*np.pi/30*t)
Vy=V*np.cos(2*np.pi/30*t)
Om=O*np.ones_like(t)
psi=O*t+np.pi/2

VL=Vx*np.cos(psi)+Vy*np.sin(psi)
VT=-Vx*np.sin(psi)+Vy*np.cos(psi)

R=0.05
l=0.150
h=0.235

w1=1/R*(VL-VT-(1+h)*Om)
w2=1/R*(VL+VT+(1+h)*Om)
w3=1/R*(VL+VT-(1+h)*Om)
w4=1/R*(VL-VT+(1+h)*Om)


k=1.05


w1u=1/R*(VL-k*VT-(k+h)*Om)
w2u=1/R*(VL+k*VT+(k+h)*Om)
w3u=1/R*(VL+k*VT-(k+h)*Om)
w4u=1/R*(VL-k*VT+(k+h)*Om)


wi=np.vstack([w1,w2,w3,w4])
wiu=np.vstack([w1u,w2u,w3u,w4u])
vlvtom=np.vstack([VL,VT,Om])

np.savetxt('laba4_wi.txt',wi)
np.savetxt('laba4_wiu.txt',wiu)
np.savetxt('laba4_vlvtom.txt',vlvtom)

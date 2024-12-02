from numpy import sqrt,sin,cos, savetxt,pi,arctan
import matplotlib.pyplot as plt
from circles import *
dt=0.05
V=0.15
T=14.65
past_coord=[0,0]
past_time=0
L=T*V
#X=L*0.3
#Y=L*0.4
R=0.35
coords=get_circle_coord(R, 100, 0,R,3/2*pi) # [[X,0],[X,Y],[0,0]]#[[-0.1,0.23],[0,0.56],[0.1,0.23],[0,0]]
Vx=[]
Vy=[]
Om=[]
om=-V/R
psi_plat=0
for coord in coords:
    dX=coord[0]-past_coord[0]
    dY=coord[1]-past_coord[1]
    ddXY=sqrt(dX*dX+dY*dY)
    print(dX," ",dY)
    for t in range(round(ddXY/V/dt)):
        psi=arctan_mod(dX,dY)-psi_plat
        Vx.append(V*cos(psi))
        Vy.append(V*sin(psi))
        Om.append(om)
        psi_plat=psi_plat+om*dt
    past_coord=coord
    past_time=past_time+ddXY/V

data = [[Vx[i], Vy[i], Om[i]] for i in range(len(Vx))]

savetxt('lab3_pereverzev_12e.txt', data, fmt='%.5f')

Xc=[0]
Yc=[0]
lenA=0.1
Xa=[lenA]
Ya=[0]
psi=[0]
for i in range(1, len(Vx)):
    Xc.append(Xc[i-1]+Vx[i-1]*dt*cos(psi[i-1])-Vy[i-1]*dt*sin(psi[i-1]))
    Yc.append(Yc[i-1]+Vy[i-1]*dt*cos(psi[i-1])+Vx[i-1]*dt*sin(psi[i-1]))
    #print(Yc[i], " ", Vy[i])
    psi.append(psi[i-1]+Om[i-1]*dt)
    Xa.append(Xc[i]+lenA*cos(psi[i]))
    Ya.append(Yc[i]+lenA*sin(psi[i]))
plt.plot(Xc,Yc)
plt.plot(Xa,Ya)

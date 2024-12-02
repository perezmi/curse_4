import numpy as np
import matplotlib.pyplot as plt

dt=0.05
mod="lab2"
#plt.figure(figsize=[150,200])

def integra_XYPsi(Vt,Vl,Om):
    X=np.zeros_like(Vt)
    Y=np.zeros_like(Vl)
    Psi=np.zeros_like(Om)
    for i in np.arange(1,len(Vt)):
        X[i]=X[i-1]+dt*(Vt[i]*np.cos(Psi[i-1])-Vl[i]*np.sin(Psi[i-1]))
        Y[i]=Y[i-1]+dt*(Vl[i]*np.cos(Psi[i-1])+Vt[i]*np.sin(Psi[i-1]))
        Psi[i]=Psi[i-1]+Om[i]*dt
        
    return [X,Y,Psi]
def simple_integra(A):
    B=np.zeros_like(A)
    for i in np.arange(0,len(A)):
        B[i]=B[i-1]+dt*A[i]
    return B
def simple_d(A):
    B=np.zeros_like(A)
    for i in np.arange(0,len(A)):
        B[i]=(A[i]-A[i-1])/dt
    return B
def square_err(E):
    err=0
    for e in E: 
        err=err+e**2
    err=err**0.5/len(E)
    return err
def sign(a):
    if type(a)==np.float64:
        if a>0:
            return 1
        else:
            return -1
    else:
        A=np.zeros_like(a)
        for i in np.arange(len(a)):
            if a[i]>0:
                A[i]=1
            else: A[i]=-1
        return A
            

[V_Tid,V_Lid,Omid]=np.genfromtxt(mod+"_pereverzev_12e.txt").T
[Xid,Yid,Psiid]=integra_XYPsi(V_Tid,V_Lid,Omid)
plt.plot(Xid,Yid)

[V_Treal,V_Lreal,Omreal]=np.genfromtxt(mod+"_pereverzev_12e_out.txt").T[9:12,1:]
[Xreal,Yreal,Psireal]=integra_XYPsi(V_Treal,V_Lreal,Omreal)
plt.plot(Xreal,Yreal)
plt.grid(True)
plt.legend(["Траектория по идеальным данным","Траектория по реальным данным"],loc="upper left",fontsize="5")
plt.xlabel("X, м")
plt.ylabel("Y, м")
plt.savefig(mod+'trajectory.png')
plt.close()
#Отклонения скоростей:
t=np.arange(0,(len(V_Tid))*0.05,0.05)
plt.plot(t,V_Tid)
plt.plot(t,V_Treal)#-V_Treal)
plt.grid(True)
plt.legend(["Теоретические данные","Реальные данные"],loc="upper left",fontsize="5")
plt.ylabel("V_T, м/с")
plt.xlabel("t, с")
plt.savefig(mod+'V_T.png')
plt.close()


plt.plot(t,V_Lid)
plt.plot(t,V_Lreal)#-V_Treal)
plt.grid(True)
plt.legend(["Теоретические данные","Реальные данные"],loc="upper left",fontsize="5")
plt.ylabel("V_L, м/с")
plt.xlabel("t, с")
plt.savefig(mod+'V_L.png')
plt.close()

plt.plot(t,Omid)
plt.plot(t,Omreal)#-V_Treal)
plt.grid(True)
plt.legend(["Теоретические данные","Реальные данные"],loc="upper left",fontsize="5")
plt.ylabel("Om, рад/с")
plt.xlabel("t, с")
plt.savefig(mod+'Om.png')
plt.close()

#Ошибки по скорости
V_Terr=V_Tid-V_Treal
V_Lerr=V_Lid-V_Lreal
Om_err=Omid-Omreal


plt.figure(figsize=(5,9))
plt.subplot(3,1,1)
plt.plot(t,V_Terr)
plt.grid(True)
plt.xlabel("t,c")
plt.ylabel("Ошибка V_T")

plt.ylabel("Ошибка V_T")
plt.subplot(3,1,2)
plt.plot(t,V_Lerr)
plt.grid(True)
plt.xlabel("t,c")
plt.ylabel("Ошибка V_L")

plt.subplot(3,1,3)
plt.plot(t,Om_err)
plt.grid(True)
plt.xlabel("t,c")
plt.ylabel("Ошибка Om")
plt.savefig(mod+"V_err")
plt.close()
#Ошибки по перемещению:
X_err=simple_integra(V_Terr)
Y_err=simple_integra(V_Lerr)
Psi_err=simple_integra(Om_err)

plt.figure(figsize=(5,9))
plt.subplot(3,1,1)
plt.plot(t,X_err)
plt.grid(True)
plt.xlabel("t,c")
plt.ylabel("Ошибка X")

plt.subplot(3,1,2)
plt.plot(t,Y_err)
plt.grid(True)
plt.xlabel("t,c")
plt.ylabel("Ошибка Y")

plt.subplot(3,1,3)
plt.plot(t,Psi_err)
plt.grid(True)
plt.xlabel("t,c")
plt.ylabel("Ошибка Psi")
plt.savefig(mod+"X_err")
plt.close()

        
M=np.genfromtxt(mod+"_pereverzev_12e_out.txt").T[5:9,1:]
R=0.25
Om=np.genfromtxt(mod+"_pereverzev_12e_out.txt").T[1:5,1:]
Phi=np.zeros_like(M)
V_Lreald=simple_d(V_Lreal)
V_Treald=simple_d(V_Treal)
p=[]
F_L=1/R*(M[0,:]+M[1,:]+M[2,:]+M[3,:])
F_T=1/R*(-M[0,:]+M[1,:]+M[2,:]-M[3,:])
b=np.array([F_L,F_T])
h=[]
bb=[]
for i in np.arange(len(V_Lreal)):
    h.append([V_Lreald[i],   V_Lreal[i],    0,              1/R*(sign(Om[0,i])+sign(Om[1,i])+sign(Om[2,i])+sign(Om[3,i])),  0])
    h.append([V_Treald[i],   0,          V_Treal[i],     1/R*(-sign(Om[0,i])+sign(Om[1,i])+sign(Om[2,i])-sign(Om[3,i])), 4*2**0.5/0.5*sign(V_Treal[0])])
    bb.append(b[0,i])
    bb.append(b[1,i])
    H=np.array([
        [V_Lreald[i],   V_Lreal[i],    0,              1/R*(sign(Om[0,i])+sign(Om[1,i])+sign(Om[2,i])+sign(Om[3,i])),  0],
        [V_Treald[i],   0,          V_Treal[i],     1/R*(-sign(Om[0,i])+sign(Om[1,i])+sign(Om[2,i])-sign(Om[3,i])), 4*2**0.5/0.5*sign(V_Treal[0])]
        ])
    p.append(np.linalg.lstsq(H, b[:,i])[0])

p=np.array(p)

P=np.linalg.lstsq(h, bb)[0]

plt.subplot(2,1,1)
plt.plot(t[:],p[:,3])
plt.plot([t[0],t[len(t)-1]],[P[3],P[3]])
plt.xlabel("t,с")
plt.ylabel("F1")

plt.subplot(2,1,2)
plt.plot(t,p[:,4])
plt.plot([t[0],t[len(t)-1]],[P[4],P[4]])
plt.xlabel("t,с")
plt.ylabel("F2")

plt.savefig(mod+'F.png')
plt.close()

#Среднеквадратичное отклонение:

print("Отклонение по продольной скорости:", square_err(V_Terr),"м/с\n",
      "Отклонение по перпендикулярной скорости:", square_err(V_Lerr),"м/с\n",
      "Отклонение по скорости вращения по оси Z:",square_err(Om_err),"рад/с\n",
      "Отклонение по продольному перемещению:",square_err(X_err),"м\n",
      "Отклонение по перпендикулярному перемещению:",square_err(Y_err),"м\n",
      "Отклонение по вращению вокруг оси Z",square_err(Psi_err),"рад\n",
      "p:",str(P))
with open(mod+'_err.txt', 'w') as f:
    for l in ["Отклонение по продольной скорости:", str(square_err(V_Terr)),"м/с\n",
          "Отклонение по перпендикулярной скорости:", str(square_err(V_Lerr)),"м/с\n",
          "Отклонение по скорости вращения по оси Z:",str(square_err(Om_err)),"рад/с",
          "Отклонение по продольному перемещению:",str(square_err(X_err)),"м\n",
          "Отклонение по перпендикулярному перемещению:",str(square_err(Y_err)),"м\n",
          "Отклонение по вращению вокруг оси Z",str(square_err(Psi_err)),"рад\n",
          "p:",str(P)]:    
        f.write(l)
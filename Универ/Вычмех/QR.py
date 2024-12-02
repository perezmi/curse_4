import numpy as np


A=np.array([[-18.0,0,30,-12],
            [9,10,39,-8],
            [36,24,12,48],
            [-18,-9,1,5]])
b=np.array([6,95,108,-43])

def reflection(A):
    m, n = A.shape
    print("A:",A)
    Q = np.eye(m)
    R = A.copy()
    #y=b.copy()
    for i in range(n-1):
        print("\n\ni:",i)
        x = R[i:, i]
        e1 = np.zeros_like(x)
        e1[0] = np.linalg.norm(x)
        u = (x - e1)
        u=u/np.linalg.norm(u)
        
        H = np.eye(m)
        H[i:, i:] -= 2 * np.outer(u, u)#/ np.linalg.norm(u)
        #sy=y@H
        #print("y:",y)
        print("H:",clean(H))
        R = H @ R
        print("Q:\n",Q)
        Q = Q @ H.T
        
    return Q, R

def solve_uppertreg(l,U):
    res=np.zeros_like(l)
    for i in np.arange(len(l)-1,-1,-1):
        summ=0
        for k in np.arange(len(l)-1,i,-1):
            summ=summ+res[k]*A[i,k]
        res[i]=(l[i]-summ)/U[i,i]
    return res
def solve_undertreg(l,U):
    res=np.zeros_like(l)
    for i in np.arange(len(l)):
        summ=0
        for k in np.arange(i):
            summ=summ+res[k]*A[i,k]
        res[i]=(l[i]-summ)/1
    return res

def clean(A):
    B=A.copy()
    for i in range(len(B)):
        for j in range(len(B[i])):
            if np.abs(B[i,j])<0.0001:
                B[i,j]=0
    return B

Q,R=reflection(A)
X=np.linalg.solve(R,b@Q)
print("X:",X)
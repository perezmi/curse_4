import matplotlib.pyplot as plt
import numpy as np

def f(x): return x**3+4*x**2-10
def sign(x):
    if x>0: return 1
    if x<0: return -1
def search(a,b,eps):
    c=b
    cold=a
    dc=a-b
    dcold=dc
    k=0
    q=0.9
    while ((1-q)/q*eps<abs(dc)):
        cold=c
        c=(a*f(b)-b*f(a))/(f(b)-f(a))
        dcold=dc
        dc=c-cold
        k+=1
        q=abs(dc/dcold)
        print(k)
        if sign(f(c))==sign(f(b)):
            b=c
        else:
            a=c
    return c

a=1
b=2
eps=10**(-6)
ans=search(a,b,eps)
print(ans)
X=np.arange(-3,3,0.01)
Y=f(X)
plt.plot(X,Y)
plt.plot(ans,f(ans),'*')
plt.grid(True)
plt.show()

import numpy as np
import matplotlib.pyplot as plt
def inverse_parabolic_interpolation(f, x0, x1,epsilon=1e-8, max_iterations=100):
    x2=(x0+x1)/2
    f0, f1,f2 = f(x0), f(x1),f(x2)
    for i in range(max_iterations):
        x3 = x0*f1*f2/((f0-f1)*(f0-f2))+f0*x1*f2/((f1-f0)*(f1-f2))+f0*f1*x2/((f2-f0)*(f2-f1))
        f3 = f(x3)
        if abs(f2) < epsilon:
            return x3,i
        x0,x1,x2=x1,x2,x3
        f0,f1,f2=f1,f2,f3


# Пример использования
def f(x):
    return np.log(x*x+1)-np.exp(0.4*x)*np.cos(np.pi*x)

x0=-1
x1=0
n=0
X=np.arange(-5,6,0.01)
Y=f(X)
plt.plot(X,Y)
plt.grid(True)

while(n<5):
    n=n+1
    [result,i] = inverse_parabolic_interpolation(f, x0,x1,epsilon=1e-12)
    print(x0," ",x1,": ",result," ",i)
    if result: plt.plot(result,f(result),".")
    x0=x0+1
    x1=x1+1
    

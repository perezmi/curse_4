import numpy as np

A=np.array([[-18,    0,   30, -12],
            [9,      10,  39, -8],
            [36,     24,  12, 48],
            [-18.0,  -9,   1, 5]])
            
b=np.array([6.0,95,108,-43])
for j in range(len(A)):
    print("\n\nРассмотрим столбец:",j+1)
    St=A[0:4,j]
    for i in range(len(St)):
        sum_str=""
        summ=0
        if i<j:
            for k in range(i):
                summ=summ+A[i,k]*A[k,j]
                sum_str=sum_str+str(A[i,k])+"*"+str(A[k,j])+"+"
        else:
            for k in range(j):
                sum_str=sum_str+str(A[i,k])+"*"+str(A[k,j])+"+"
                summ=summ+A[i,k]*A[k,j]
        print("U[",i+1,",",j+1,"]=",A[i,j],"-(",sum_str,")=",A[i,j]-summ)
        A[i,j]=	A[i,j]-summ
    print("\nПолучившаяся матрица:\n",A)
    t=np.argmax(abs(St[j:len(A)]))+j
    buf=np.array(A[t,0:4])
    A[t,0:4]=A[j,0:4]
    A[j,0:4]=buf
    b[t],b[j]=b[j],b[t]
    print("Перестанавливаем строки:\n",A)
    print("Перестанавливаем строки в матрице b:\n",b)
    for k in range(j+1,len(A)): 
        St[k]=St[k]/St[j]
    print("Делим элементы матрицы l на ведущий элемент:\n",A)

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
Y=solve_undertreg(b,A)
X=solve_uppertreg(Y,A)
print("U*Y=b\nY:",Y)
print("L*X=Y,\nX:",X)

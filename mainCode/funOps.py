import numpy as np
from typing import Any, Callable, Iterable
from operator import ne as NE
from functools import reduce as Red

# Tacit
def T(*g:Callable)->Callable:
    """
    used for making APL-like code
    ```
    average=T(sum,div,len)
    ```
    instead of:
    ```
    average=lambda x:sum(x)/len(x)
    ```
    """
    def outputFunc(*a)->Callable:
        if not g:
            return a[0]
        
        if len(g)<3: 
            return T(*g[:-1])(g[-1](*a))

        leftFunc   = g[-3](*a)
        rightFunc  = g[-1](*a)
        middleFunc = g[-2]

        joinedFuncs = middleFunc(leftFunc,rightFunc)
        restOfFunc  = T(*g[:-3],C(joinedFuncs))
        return restOfFunc(*a)

    return outputFunc

# Partition ⊆
def Parti(x:Iterable,y:Iterable):
    temp=[[]]
    for i,j in zip(x,y):
        if i:temp[-1]+=[j]
        else:temp    +=[[]]
    return temp

def Curry(f:Callable,*x,**xx)->Callable:
    def g(*y,**yy):
        yl=list(y)
        return f(*([yl.pop,C(i)][i!=Any]() for i in x),*yl,**yy,**xx)
    return g

# Æ inverts inputs to function. 
# f(x,y) == Æ(f)(y,x)
def Æ(f:Callable):
    "Inverts arguments of function"
    return lambda*x,**a:f(*x[::-1],**a)

# Constant, 
# C(x)(123,a=31) == x
def C(x):
    return lambda*_,**a:x

# Apply all functions in a row
# DFN(f,g,h,k)(x) == f(g(h(k(x))))
DFN=lambda*f:lambda*a:DFN(*f[:-1])(f[-1](*a))if f else a[0]
Enc=lambda*x:x
X=  lambda*x:x[0]
Y=Æ(X)


Over=lambda f,g:T(T(g,X),f,T(g,Y))
Pick=lambda x:x[0]
Red2=lambda f:lambda*x:Red(f,x)if len(x)!=1 else f(x[0])
def E(f):
    def g(*x):
        return np.reshape(np.array(Red2(Curry(Map,f))(*Map(Ravel,x)),object),Shape(x[0]))
    return g
Check=Curry(T,Any,X,C("Check:"),print,Enc)
# print(1+Check(Add)(1,3))

Map=T(tuple,map)
def Split(x:list,y):
    a=E(Curry(NE,y))(x)
    return Parti(a,x)

NPArr = T(X,np.array,C(object))
Shape = T(np.shape,NPArr)
Ravel = T(np.ravel,NPArr)

# def Shape(x):return np.shape(np.array(x,object))
# def Ravel(x):return np.ravel(np.array(x,object))

Print=T(X,X,print)

def f(g):return lambda*x:g(*x[::-1])

@f
def minus(x,y): return x-y

print(minus(5,6))
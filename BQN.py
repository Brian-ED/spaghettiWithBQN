import subprocess
from typing import Callable

def BQN(*args:str):
    process = subprocess.Popen(["BQN",".bqn",*args], stdout=subprocess.PIPE,text=1)
    output, error = process.communicate()
    if error:
        raise Exception(error)
    return output

def BQNfn(bqnFunc:str)->Callable:
    return lambda x:BQN('dfn',bqnFunc,x)

if __name__ == "__main__":

    spaces=BQNfn("{' '=𝕩}")
    print('where are spaces?: ',spaces('something a dwa'))

    mean=BQNfn("fns.Mean")
    print("What's the mean?: ",mean('⟨1,2,3⟩'))

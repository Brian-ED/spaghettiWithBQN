import subprocess
from typing import Callable, Iterable, Union

def BQN(*args:str):
    process = subprocess.Popen(["BQN","main.bqn",*args], stdout=subprocess.PIPE,text=1)
    output, error = process.communicate()
    if error:
        raise Exception(error)
    return output

def BQNfn(bqnFunc:str)->Callable:
    """
    The returned function only supports input of type:
        str
        Iterable[str] 
    """
    
    def f(x:Union[str,Iterable[str]]):
        if type(x)==str:
            typeOfInput='dfn'
        elif all(isinstance(i,str) for i in x):
            typeOfInput='dfn strlist'
        else:
            raise Exception("Type was not recognized in BQN function:\n"+bqnFunc)

        return BQN(typeOfInput,bqnFunc,*([x] if type(x)==str else x))
    return f



if __name__ == "__main__":

    testing={
        'BQN'  :0,
        'BQNfn':0,
    }

    if testing['BQN']:
        print(BQN('dfn strlist','fns.Join','Nest\\ed','li\'\"st','of','strings'))

    if testing['BQNfn']:

        spaces=BQNfn("{' '=𝕩}")
        print('where are spaces?: ',spaces('something a dwa'))

        mean=BQNfn("fns.Mean")
        print("What's the mean?: ",mean('⟨1,2,3⟩'))

        join=BQNfn('fns.Join')
        print("Strings joined: ",join(['Nest\\ed','li\'\"st','of','strings']))

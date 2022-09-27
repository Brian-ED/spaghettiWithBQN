from functools import reduce
from math import prod
import subprocess
from time import sleep
from typing import Callable, Iterable, Union
import numpy as np

class char:
    def __init__(self,character):
        if len(character)!=1:
            raise Exception("Invalid length for character")
        self.character=character

    def __str__(self) -> str:
        return self.character

    def __repr__(self) -> str:
        return "char('"+self.character+"')"

def charArrToStr(x):
    return ''.join(map(str,np.ravel(x)))


def BQN(*args:str):
    process = subprocess.Popen(["BQN","/home/brian/personal/code/py/spaghettiWithBacon/code/main.bqn",*args], stdout=subprocess.PIPE,text=1)
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

    def f(x:Union[str,Iterable[str]])->str:
        if type(x)==str:
            typeOfInput='dfn'
        elif all(isinstance(i,str) for i in x):
            typeOfInput='dfn strlist'
        else:
            raise Exception("Type was not recognized in BQN function:\n"+bqnFunc)

        return BQN(typeOfInput,bqnFunc,*([x] if type(x)==str else x))
    return f

def BQNEval():
    """
    Used for straightup evaluating BQN, no fuss.
    """

def PrefixedInteger(types:str) -> tuple[int,int]:
    x=1
    lenOfArg=1+sum((x:=x and i in "0123456789" for i in types[1:]))
    listLen=int(types[1:lenOfArg])
    return lenOfArg,listLen


def CollapseInts(t:str) -> list[Union[str,list[int]]]:
    types=str(t)
    done=[]
    while ""!=types:
        if types[0]=='l':
            lenOfArg,listLen=PrefixedInteger(types)

            done+=[[]]
            done[-1]+=[listLen]
            types=types[lenOfArg:]

            while types[0]==' ':
                lenOfArg,listLen=PrefixedInteger(types)
                done[-1]+=[listLen]
                types=types[lenOfArg:]
        else:
            done+=types[0],
            types=types[1:]
    return done

def SmartReshape(x,shape):
    if len(shape)==1:
        if all((type(i)==char for i in x[:shape[0]])):
            r=charArrToStr(x[:shape[0]])
        else:
            return tuple(x[:shape[0]])
    else:
        r=np.reshape(np.array(x[:prod(shape)],object),shape)
    return r

def GroupTypes(t:list[Union[str,list[int]]],args:list[str]):
    types=list(t)
    done=[]
    funcMap={'n':int,'s':str,'c':char,'f':BQNEval,'F':eval}
    while types!=[]:
        if type(types[0])==list:
            done=[SmartReshape(done,types[0])]+done[prod(types[0]):]
            types=types[1:]
        else:
            done=[funcMap[types[0]](args[0])]+done
            args,types=args[1:],types[1:]
    return tuple(done)

def Handler(allArgs:list[str]):
    types=allArgs[0]
    args=allArgs[1:]
    return GroupTypes(CollapseInts(types)[::-1],args[::-1])


print(Handler(["l3l3 4ccccccccccccl2 3nnnnnnl5ccl3sl2nnnnl3ccc","t","h","i","s","i","s"," ","a","t","e","s","t","1","2","3","4","5","6","a","b","nested","3","2","1","2","s",'u','m']))


if __name__ == "__main__":

    testing={
        'BQN'               :0,
        'BQNfn'             :0,
        'PrefixedInteger'   :0,
        'CollapseInts'      :0
    }

    if testing['BQN']:
        # Nest\edli'"stofstrings
        print(BQN('dfn strlist','fns.Join','Nest\\ed','li\'\"st','of','strings'))

    if testing['BQNfn']:

        # ⟨ 0 0 0 0 0 0 0 0 0 1 0 1 0 0 0 ⟩
        spaces=BQNfn("{' '=𝕩}")
        print('where are spaces?: ',spaces('something a dwa'))

        # 2
        mean=BQNfn("fns.Mean")
        print("What's the mean?: ",mean('⟨1,2,3⟩'))

        # Nest\edli'"stofstrings
        join=BQNfn('fns.Join')
        print("Strings joined: ",join(['Nest\\ed','li\'\"st','of','strings']))
    
    if testing['PrefixedInteger']:
        # (3,11)
        print(PrefixedInteger("l11 22 3"))

    if testing['CollapseInts']:
        # ['s', [3, 3, 3], 's', 's', [2], 'n', 'n', 'n', 'n']
        print(CollapseInts("sl3 3 3ssl2nnnn"))

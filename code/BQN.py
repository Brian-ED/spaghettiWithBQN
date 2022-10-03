from math import prod
import subprocess
from typing import Callable, Union
import numpy as np

pathToFile='/'+'/'.join('\\'.join(__file__.split('/')).split('\\')[:-1])+'/'

class char:
    def __init__(self,character):
        if len(character)!=1:
            raise Exception(f'Invalid length for character: "{character}"')
        self.character=character

    def __str__(self) -> str:
        return self.character

    def __repr__(self) -> str:
        return "char('"+self.character+"')"

def charArrToStr(x):
    return ''.join(map(str,np.ravel(x)))

def Print(x):
    print(x)
    return x

def BQN(*args:str):
    process = subprocess.Popen(["BQN",pathToFile+"main.bqn",*args], stdout=subprocess.PIPE,text=1)
    output, error = process.communicate()
    if error: raise Exception(error)
    return Handler(eval(output))

def BQNfn(bqnFunc:str)->Callable:
    return lambda x,y=None:BQN(bqnFunc,*PyToMediary((x,y))) if y!=None else BQN(bqnFunc,*PyToMediary((x,)))

def BQNEval(arg:str):
    process = subprocess.Popen(["BQN",pathToFile+"main.bqn",arg], stdout=subprocess.PIPE,text=1)
    output, error = process.communicate()
    if error: raise Exception(error)
    return Handler(eval(output))

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
    funcMap={'n':int,'s':str,'c':char,'f':BQNfn,'F':eval}
    for i in types:
        if type(i)==list:
            done=[SmartReshape(done,i)]+done[prod(i):]
        else:
            done=[funcMap[i](args[0])]+done
            args=args[1:]
    return done[0]

def Handler(allArgs:list[str]):
    types=allArgs[0]
    args=allArgs[1:]
    return GroupTypes(CollapseInts(types)[::-1],args[::-1])

def PyToMediary(x):
    types=""
    args=()
    scalers={str:'s',char:'c',int:'n',np.int64:'n'}
    while len(x)>0:
        t=type(x[0])
        if t in scalers:
            types+=scalers[t]
            args+=x[0],
            x=x[1:]
        elif t in{tuple,list}:
            types+='l'+str(len(x[0]))
            x=*x[0],*x[1:]
        else: # assuming last type is numpy array, just for now
            types+='l'+' '.join(map(str,np.shape(x[0])))
            x=tuple(np.ravel(x[0]))+x[1:]
    return types,*map(str,args)

if __name__ == "__main__":
    x=((
        np.reshape([*map(char,("t","h","i","s","i","s"," ","a","t","e","s","t"))],(3,4)),
        np.array((
         (1,2),
         (3,4),
         (5,6))
        ),
        (char('a'),char('b'),("nested",(3,2),1),2,3)
    ),)
    y="l3l3 4ccccccccccccl3 2nnnnnnl5ccl3sl2nnnnn","t","h","i","s","i","s"," ","a","t","e","s","t","1","2","3","4","5","6","a","b","nested","3","2","1","2","3"

    testing={
        'BQN'               :0,
        'BQNfn'             :0,
        'PrefixedInteger'   :0,
        'CollapseInts'      :0,
        'Handler'           :0,
        'PyToMediary'       :0
    }

    if testing['BQN']:
        # Nest\edli'"stofstrings
        print("Strings joined: ",BQN('∾´','l4ssss','Nest\\ed','li\'\"st','of','strings'))

    if testing['BQNfn']:
        print(BQNfn("∾")((1,2,3),(2,3,4)))

        equal=BQNfn("=")
        print('where are spaces?: ',equal(char(' '),'something a dwa'))

        mean=BQNfn("+´÷≠")
        print("What's the mean?: ",mean((1,2,3)))

        join=BQNfn('∾´')
        print("Strings joined: ",join(['Nest\\ed','li\'\"st','of','strings']))


    
    if testing['PrefixedInteger']:
        # (3,11)
        print(PrefixedInteger("l11 22 3"))

    if testing['CollapseInts']:
        # ['s', [3, 3, 3], 's', 's', [2], 'n', 'n', 'n', 'n']
        print(CollapseInts("sl3 3 3ssl2nnnn"))

    if testing['Handler']:
        print(Handler(["l3l3 4ccccccccccccl2 3nnnnnnl5ccl3sl2nnnnl3ccc","t","h","i","s","i","s"," ","a","t","e","s","t","1","2","3","4","5","6","a","b","nested","3","2","1","2","s",'u','m']))
    
    if testing["PyToMediary"]:
        æ=PyToMediary(x)
        print("PyToMediary result: ",æ)
        print("Intended output?: ",y==æ)
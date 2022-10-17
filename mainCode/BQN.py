import asyncio
import os
import subprocess
from typing import Callable, Union
import numpy as np
from os import system as SH
from time import sleep
pathToFile='/'+'/'.join('\\'.join(__file__.split('/')).split('\\')[:-1])+'/'

class char:
    def __init__(self,character):
        if len(character)!=1:
            raise Exception(f'Invalid length for character: "{character}"')
        self.character=character

    def __str__(self) -> str:
        return self.character

    def __repr__(self) -> str:
        return f"char('{self.character}')"

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
            r=''.join(map(str,np.ravel(x[:shape[0]])))
        else:
            return tuple(x[:shape[0]])
    else:
        r=np.reshape(np.array(x[:np.prod(shape)],object),shape)
    return r

def GroupTypes(t:list[Union[str,list[int]]],args:list[str]):
    types=list(t)
    done=[]
    funcMap={
        'n':(lambda x:int(x) if 0==float(x)%1 else float(x)),
        's':str,
        'c':char,
        'f':BQNfn,
        'F':eval}
    for i in types:
        if type(i)==list:
            done=[SmartReshape(done,i)]+done[np.prod(i):]
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
        elif t==bool:
            types+='n'
            args+=int(x[0]),
            x=x[1:]
        elif t in{tuple,list}:
            types+='l'+str(len(x[0]))
            x=*x[0],*x[1:]
        elif t==np.ndarray:
            types+='l'+' '.join(map(str,np.shape(x[0])))
            x=tuple(np.ravel(x[0]))+x[1:]
        else: raise Exception("Type not recognized by BQN")
    return types,*map(str,args)

def StartBQNScript(path:str):
    SH(f'BQN "{path}"')

def ToBQNList(pyList:list[str]):
    return '⟨'+','.join(['"'+i.replace('"','""')+'"' for i in pyList])+'⟩'

    

class Communication:

    def __init__(self,id:str,pathToBQN:str=''):
        self.commPath="communication/"+id
        if pathToBQN:
            StartBQNScript(pathToBQN)
        self.coro=None
    
    def SendMsg(self,msg:str):
        path=f"{self.commPath}/msgFromBQN{len(os.listdir(self.commPath))}.txt"
        with open(path,"w") as f:
            f.write(ToBQNList(PyToMediary(msg)))
    
    def GetMsg(self,wait=False):
        FindFile=lambda x:[i.startswith("msgFromBQN") for i in os.listdir(x)]
        m=FindFile(self.commPath)
        while wait and not any(m):
            sleep(0.2)
            m=FindFile(self.commPath) 
        if any(m):
            raise Exception("No msg found. Please do 'GetMsg 1' if expected to wait for msg")
        file=sorted([i for i in zip(m,os.listdir(self.commPath)) if m])[0]
        with open(file) as f:
            r=Handler(f.read())
        os.remove(file)
        return r
    
    def GetMsgAsync(self,coro:function):
        """A decorator that executes a function every message.

        The events must be a :ref:`coroutine <coroutine>`.

        Example
        ---------
        ```
        from BQN.BQN import Communication
        comm=Communication("hello")
        
        @comm.GetMsgAsync
        async def OnMsgGotten(msg):
            print(msg)
        ```
        """
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError('event registered must be a coroutine function')
        self.coro=coro
        return coro

    def BQNExec(self,msg:str,action:str=""):
        availableActions="exec","value"
        if action not in availableActions:
            raise Exception(f"The action was not recognized.\nValid: {availableActions}\nInvalid: {action}")
        with open(action+'.bqn', 'w') as fp:
            fp.write(msg)

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
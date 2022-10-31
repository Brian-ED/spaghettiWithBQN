import asyncio
from functools import reduce
from math import inf, nan
import os
import subprocess
from typing import Any, Callable, Union
import numpy as np
from os import system as SH
from time import sleep, time_ns
pathToFile='/'.join('\\'.join(__file__.split('/')).split('\\')[:-1])+'/'

Print=lambda x:(x,print(x))[0]
class char:
    def __init__(self,character:str):
        if len(character)!=1:
            raise Exception(f'Invalid length for character: "{character}"')
        self.character=character

    def __str__(self) -> str:
        return self.character

    def __repr__(self) -> str:
        return f"char('{self.character}')"

def BQN(*args:str)->Any:
    process = subprocess.Popen(["BQN",pathToFile+"main.bqn",*args], stdout=subprocess.PIPE,text=True)
    output, error = process.communicate()
    if error: raise Exception(error)
    print(output)
    return Handler(eval(output))

def BQNfn(bqnFunc:str)->Callable[[Any,Any],Any]:
    def f(x:Any,y:Any=None)->Any:
        return BQN(bqnFunc,*PyToMediary((x,y))) if y!=None else BQN(bqnFunc,*PyToMediary((x,)))
    return f

def BQNEval(arg:str)->Any:
    process = subprocess.Popen(["BQN",pathToFile+"main.bqn",arg], stdout=subprocess.PIPE,text=True)
    output, error = process.communicate()
    if error: raise Exception(error)
    return Handler(eval(output)) # type: ignore

def PrefixedInteger(types:str) -> tuple[int,int]:
    x=1
    lenOfArg=1+sum((x:=x and i in "0123456789" for i in types[1:]))
    listLen=int(types[1:lenOfArg])if 1!=lenOfArg else None
    return lenOfArg,listLen

def CollapseInts(t:str) -> list[Union[str,list[int]]]:
    types=str(t)
    done=[]
    while ""!=types:
        if types[0]=='l':
            done+=[[]]
            lenOfArg,listLen=PrefixedInteger(types)
            types=types[lenOfArg:]
            if listLen!=None:
                done[-1]+=[listLen]
            
                while types[0]==' ':
                    lenOfArg,listLen=PrefixedInteger(types)
                    done[-1]+=[listLen]
                    types=types[lenOfArg:]
        else:
            done+=types[0],
            types=types[1:]
    return done


def Handler2(allArgs:str) -> list[Union[str,list[int]]]:
    types=allArgs[0]
    args=allArgs[1:]
    def Func(𝕩,𝕨):
        if 𝕨=='l':
            # (-+´𝕩∊' '∾'0'+↕10)(ToNums∘↑(⥊<∘⥊)⌽∘↓)𝕩
            
            # (-+´𝕩∊' '∾'0'+↕10)
            shapeLen=-sum(i in' 0123456789'for i in 𝕩)
            # shapeLen         (ToNums∘↑(⥊<∘⥊)⌽∘↓)𝕩

            #                   ToNums∘↑
            shape=[int(i) for i in 𝕩[shapeLen:]]
            # shapeLen         (shape   (⥊<∘⥊)⌽∘↓)𝕩

            #                                 ⌽∘↓
            nonShape=𝕩[:shapeLen:-1]
            # shapeLen         (shape   (⥊<∘⥊)nonShape)𝕩
            
            # shape (⥊<∘⥊) nonShape
            return [SmartReshape(nonShape,shape)]
        return 𝕨+𝕩
    typesInShape=reduce(Func,types,())
    GroupTypes(typesInShape,args)

"""
    types ←⊑𝕩
    args ←1↓𝕩
    
    typesInShape←⊑⟨⟩≡⟜'l'◶⟨
      ∾˜
      {-+´𝕩∊' '∾'0'+↕10}(ToNums∘↑(⌽<∘⥊∾×´⊸↓)⌽∘↓)⊢
    ⟩´types

    args GroupTypes typesInShape
"""


def SmartReshape(x:Any,shape:tuple[int])->Any:
    if len(shape)==1:
        if all((type(i)==char for i in x[:shape[0]])):
            r=''.join(str(i) for i in x[:shape[0]])
        else:
            r=tuple(x[:shape[0]])
    else:
        r=np.reshape(np.array(x[:int(np.prod(shape))],object),shape)
    return r

def GroupTypes(types:list[Union[str,list[int]]],args:list[str]):
    done=[]
    def ToNumber(x:str):
        y=x.replace("¯","-").replace("∞","inf")
        return int(x) if 0==float(y)%1 else float(y)
    funcMap:dict[str,Callable[[str],Any]]={
        'n':ToNumber,
        's':str,
        'c':char,
        'f':BQNfn,
        'F':eval}
    for i in types:
        if type(i)==list:
            done=[SmartReshape(done,i)]+done[int(np.prod(i)):]
        else:
            done=[funcMap[str(i)](args[0])]+done
            args=args[1:]
    return done[0]

def Handler(allArgs:list[str]):
    types=allArgs[0]
    args=allArgs[1:]
    return GroupTypes(CollapseInts(types)[::-1],args[::-1])

def PyToMediary(arg:Any)->tuple[str]:
    x=type(arg)(arg)
    types=f"l{len(arg)}"
    args=()
    scalers:dict[Callable[[str],Any],str]={str:'s',char:'c',int:'n',np.int64:'n',bool:'n'}
    while len(x)>0:
        t=type(x[0])
        if t in scalers:
            types+=scalers[t]
            args+=(x[0],) if t!=bool else (int(x[0]),)
            x=x[1:]
        elif t in{tuple,list}:
            types+='l'+str(len(x[0]))
            x=*x[0],*x[1:]
        elif t==np.ndarray:
            types+='l'+' '.join(map(str,np.shape(x[0])))
            x=tuple(np.ravel(x[0]))+x[1:]
        else: raise Exception("Type not recognized by BQN")
    return tuple((types,*map(str,args)))

def StartBQNScript(path:str)->None:
    SH(f'BQN "{path}"')

def ToBQNList(pyList:list[str]):
    return '⟨'+','.join(['"'+i.replace('"','""')+'"' for i in pyList])+'⟩'



class Communication:

    def __init__(self,id:str,pathToBQN:str=''):
        self.commPath="comm/"+id
        if pathToBQN:
            StartBQNScript(pathToBQN)
        self.coro=None
    
    def SendMsg(self,msg:str):
        path=f"{self.commPath}/msgFromBQN{len(os.listdir(self.commPath))}.txt"
        with open(path,"w") as f:
            f.write(ToBQNList([*PyToMediary(msg)]))
    
    def GetMsg(self,wait=False):
        FindFile=lambda x:[i.startswith("msgFromBQN") for i in os.listdir(x)]
        m=FindFile(self.commPath)
        while wait and not any(m):
            sleep(0.2)
            m=FindFile(self.commPath) 
        if any(m):
            raise Exception("No msg found. Please do 'GetMsg 1' if expected to wait for msg")
        file=sorted([j for i,j in zip(m,os.listdir(self.commPath)) if i])[0]
        with open(file) as f:
            r=Handler(eval(f.read()))
        os.remove(file)
        return r
    
    def GetMsgAsync(self,coro):
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
        np.reshape([*map(char,"thisis atest")],(3,4)),
        np.array(
        ((1,2),
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
        'Handler'           :1,
        'PyToMediary'       :0
    }

    if testing['BQN']:
        # Nest\edli'"stofstrings
        print("Strings joined: ",BQN('∾´','l1l4ssss','Nest\\ed','li\'\"st','of','strings'))

    if testing['BQNfn']:
        print(BQNfn("∾")((1,2,3),(2,3,4)))

        equal=BQNfn("=")
        print('where are spaces?: ',equal(char(' '),'something a dwa'))

        mean=BQNfn("+´÷≠")
        print("What's the mean?: ",mean((1,2,3)))

        join=BQNfn('∾´')
        print("Strings joined: ",join(['Nested','list','of','strings']))

        enclose=BQNfn("<")
        print('enclose: ',enclose(char("a")))


    if testing['PrefixedInteger']:
        # (3,11)
        print(PrefixedInteger("l11 22 3abc"))

    if testing['CollapseInts']:
        # ['s', [3, 3, 3], 's', 's', [2], 'n', 'n', 'n', 'n']
        print(CollapseInts("sl3 3 3ssl2nnnn"))

    if testing['Handler']:
        #print(Handler(["l3l3 4ccccccccccccl2 3nnnnnnl5ccl3sl2nnnnl3ccc","t","h","i","s","i","s"," ","a","t","e","s","t","1","2","3","4","5","6","a","b","nested","3","2","1","2","s",'u','m']))
        print(Handler2(["l3l3 4ccccccccccccl2 3nnnnnnl5ccl3sl2nnnnl3ccc","t","h","i","s","i","s"," ","a","t","e","s","t","1","2","3","4","5","6","a","b","nested","3","2","1","2","s",'u','m']))

    if testing["PyToMediary"]:
        æ=PyToMediary(x)
        print("PyToMediary result: ",æ)
        print("Intended output?: ",y==æ)
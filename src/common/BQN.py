import asyncio
from functools import reduce as Red
from funOps import *
import os
import subprocess
from typing import Any, Callable, Union
import numpy as np
from time import sleep

# File path excluding filename
pathToFile = '/'.join(__file__.replace("\\","/").split('/')[:-1])+'/'

class char:
    def __init__(self, character:str):
        if len(character) != 1 or type(character) != str:
            raise Exception(f'Only strings of length 1 are valid characters. not: "{character}"')
        self.character = character

    __str__  = lambda s:s.character
    __repr__ = lambda s:f"char('{s.character}')"
    def __eq__(self, __o: object) -> bool:
        return self.character == str(__o)

def BQN(*args:str)->Any:
    process = subprocess.Popen(["BQN", pathToFile+"main.bqn", *args], stdout=subprocess.PIPE,text=True)
    output, error = process.communicate()
    if error: raise Exception('BQN ERROR: '+error)
    return Handler(eval(output))

def BQNfn(bqnFunc:str)->Callable[[Any, Any], Any]:
    def f(x:Any, y:Any=None)->Any:
        return BQN(bqnFunc, *(PyToMediary((x,y) if y!=None else (x,))))
    return f

def BQNEval(arg:str)->Any:
    process = subprocess.Popen(["BQN", pathToFile+"main.bqn", arg], stdout=subprocess.PIPE,text=True)
    output, error = process.communicate()
    if error: raise Exception(error)
    return Handler(eval(output))

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

def ToNum(x:str)->Union[float,int]:
    a= [float,int][0==float(x)%1](x)
    return a

funcMap:dict[str,Callable[[str],Any]]={
    'n':ToNum,
    's':str,
    'c':char,
    'f':BQNfn,
    'F':eval
}

def FromMediary(allArgs:list[str]) -> Any:
    """
    ```
    types ←⊑𝕩
    args ←1↓𝕩
    
    typesInShape←⊑⟨⟩≡⟜'l'◶⟨
      ∾˜
      {-+´𝕩∊' '∾'0'+↕10}(ToNums∘↑(⌽<∘⥊∾×´⊸↓)⌽∘↓)⊢
    ⟩´types

    args GroupTypes typesInShape
    ```
    """

    types,*args=allArgs
    def Func(𝕩:tuple,𝕨:str):
        if 𝕨=='l':
            # (-+´𝕩∊' '∾'0'+↕10)(ToNums∘↑(×´⊸↓ ⌽⊸∾ <∘⥊)⌽∘↓)𝕩
            
            # (-+´𝕩∊' '∾'0'+↕10)
            shapeLen=-sum((i in ' 0123456789') for i in 𝕩 if type(i)==str)
            # shapeLen          (ToNums∘↑(×´⊸↓ ⌽⊸∾ <∘⥊)⌽∘↓)𝕩

            #                   ToNums∘↑
            shape=*(int(''.join(i)) for i in Split(𝕩[:-shapeLen],' ')),
            # shapeLen         (shape    (×´⊸↓ ⌽⊸∾ <∘⥊)⌽∘↓)𝕩

            #                                          ⌽∘↓
            nonShape=𝕩[-shapeLen:]
            # shapeLen         (shape    (×´⊸↓ ⌽⊸∾ <∘⥊)nonShape)𝕩

            # shape (×´⊸↓ ⌽⊸∾ <∘⥊) nonShape
            return Reshape(nonShape,shape),*nonShape[int(np.prod(shape)):]
        return (𝕨,)+𝕩

    typesInShape=Red(Func,types[::-1],())
    # print(typesInShape,args)
    return (*map(tuple,GroupTypes(typesInShape,args)),)[0] # TODO simplify map[0]


def GroupTypes(typesInShape,args:list[str]):
    if type(typesInShape)==str:
        a = funcMap[typesInShape](args.pop(0))
        # print("args:",args)
        return a
    
    r = E(Curry(GroupTypes,Any,args))(typesInShape)
    if len(np.shape(r))==1:
        return*r,
    return r

def Reshape(x:Any,shape:tuple[int])->Any:
    # print('x',shape)
    # print(x)
    if len(shape)==1:
        if all(map(Curry(isinstance, Any, char), x[:shape[0]])):
            return ''.join(map(str, x[:shape[0]]))
        return *x[:shape[0]],
    return np.reshape(np.array(x[:int(np.prod(shape))],object),shape)

def Handler(allArgs:list[str]):
    types,*args=allArgs
    def GroupTypes1(
            types:list[Union[str,list[int]]],
            args:list[str]
        ):
        done=[]
        for i in types:
            if isinstance(i,(list,tuple)):
                done=[Reshape(done,i)]+done[int(np.prod(i)):]
            else:
                done=[funcMap[i](args[0])]+done
                args=args[1:]
        return done[0]
    return GroupTypes1(CollapseInts(types)[::-1],args[::-1])

scalers = {
    str:'s',
    char:'c',
    float:'n', np.float64:'n', np.float32:'n', np.float16:'n',
    int  :'n', np.int64  :'n', np.int32  :'n', np.int16  :'n', np.int8:'n', np.intp:'n',
    bool:'n', np.bool_:'n'
}

def PyToMediary(arg:Any)->tuple[str]:
    if type(arg) in scalers:
        return scalers[type(arg)], arg
    x = type(arg)(arg)
    types = f"l{len(x)}"
    args=()
    while len(x)>0:
        t=type(x[0])
        if t in scalers:
            types+=scalers[t]
            args+=x[0],
            x=x[1:]
        elif t in (tuple, list, np.ndarray):
            types+='l'+' '.join(map(str,Shape(x[0])))
            x=*Ravel(x[0]),*x[1:]
        else: raise Exception(f"Type not recognized by BQN: {t}")
    return types,*map(str,args)

def ToBQNList(pyList:list[str]):
    return '⟨'+','.join(['"'+i.replace('"','""')+'"' for i in pyList])+'⟩'

class CreateComm:

    def __init__(self,id="Default",pathToBQNScript=None):
        self.commPath="comm/"+id
        if pathToBQNScript:
            subprocess.Popen(["bqn",pathToBQNScript])

    def SendMsg(self,msg):
        path=f"{self.commPath}/msgFromPy{len(os.listdir(self.commPath))}.txt"
        with open(path,"w",encoding="utf-8") as f:
            f.write(ToBQNList(PyToMediary(msg)))
    
    def GetMsg(self,wait=False):
        FindFile=lambda:[i.startswith("msgFromBQN") for i in os.listdir(self.commPath)]
        m=FindFile()
        while wait and not any(m):
            sleep(0.2)
            m=FindFile() 
        if not any(m):
            raise Exception("No msg found. Please do 'GetMsg 1' if expected to wait for msg")
        file=self.commPath+'/'+sorted([j for i,j in zip(m, os.listdir(self.commPath)) if i])[0]
        with open(file, encoding="utf-8") as f:
            r=Handler(eval(f.read()))
        os.remove(file)
        return r
    
    coro=None
    def GetMsgAsync(self,coro):
        """A decorator that executes a function every message.

        The events must be a :ref:`coroutine <coroutine>`.

        Example
        ---------
        ```
        from BQN.BQN import Communication
        communication=comm("hello")
        
        @communication.GetMsgAsync
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
        with open(action+'.bqn', 'w', encoding="utf-8") as fp:
            fp.write(msg)

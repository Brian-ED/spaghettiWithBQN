from BQN import*
from funOps import *

# Switches to turn on/off tests
tests={
    'BQN'               :1,
    'BQNfn'             :1,
    'PrefixedInteger'   :1,
    'CollapseInts'      :1,
    'Handler'           :1,
    'fromMediary'       :1,
    'PyToMediary'       :1,
    'types'             :1,
    'communication'     :1,
}


x=(
    np.reshape([*map(char,"thisis atest")],(3,4)),
    np.array((
        (1,2),
        (3,4),
        (5,6)
    )),
    (char('a'),char('b'),("nested",(3,2),1),2,3)
)
y="l3l3 4ccccccccccccl3 2nnnnnnl5ccl3sl2nnnnn","t","h","i","s","i","s"," ","a","t","e","s","t","1","2","3","4","5","6","a","b","nested","3","2","1","2","3"
# y="l3l3 4nnnnnnnnnnnnl3 2nnnnnnl5nnl3sl2nnnnn",*map(str,range(26))

if tests['communication']:
    comm = CreateComm()
    comm.SendMsg(x)

if tests['BQN']:
    # Nest\edli'"stofstrings
    print("Strings joined: ",BQN('∾´','l1l4ssss','Nest\\ed','li\'\"st','of','strings'))

if tests['BQNfn']:
    print(BQNfn("∾")((1,2,3),(2,3,4)))

    equal=BQNfn("=")
    print('where are spaces?: ',equal(char(' '),'something a dwa'))

    mean=BQNfn("+´÷≠")
    print("What's the mean?: ",mean((1,2,3)))

    join=BQNfn('∾´')
    print("Strings joined: ",join(['Nested','list','of','strings']))

    enclose=BQNfn('<')
    print('enclose: ',enclose(char('a')))
    print('enclose: ',type(enclose(char('a'))))


if tests['PrefixedInteger']:
    print(PrefixedInteger("l11 22 3abc")==(3,11))

if tests['CollapseInts']:
    print(CollapseInts("sl3 3 3ssl2nnnn") == ['s', [3, 3, 3], 's', 's', [2], 'n', 'n', 'n', 'n'])

if tests['Handler']:
    print('success:', repr(x)==repr(Handler(y)))
    
if tests['fromMediary']:
    print(y)
    i = FromMediary(y)
    n = repr(i)==repr(x)
    if not n:
        print('i:',i)
        print('x:',x)
    print('sucess:',n)

if tests["PyToMediary"]:
    æ=PyToMediary(x)
    print("PyToMediary result:\n",æ)
    print("Intended output?:",y==æ)

if tests["types"]:
    print(BQNfn('+')(1, float('inf')))
    print(BQNfn('+')(1, float('nan')))
    print(BQNfn('+')(1, 'a'))

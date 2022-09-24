Main ←{
    "dfn"≡𝕨?
    (•BQN "fns←•Import ""/home/brian/personal/code/APL/py'n'APL test/pynapl/fns.bqn"""∾(@+10)∾⊑𝕩){𝕎𝕩}1⊑𝕩
    
}

{
    type ←⊑𝕩
    args ←1↓𝕩
    •Show type Main args
}⍟{⟨⟩≢𝕩} •args

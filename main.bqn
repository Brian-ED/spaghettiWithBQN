fnsImport←"fns←•Import ""/home/brian/personal/code/py/spaghettiWithBacon/fns.bqn"","

Main ←{
    "dfn" 𝕊 𝕩:
        (•BQN fnsImport∾⊑𝕩){𝕎𝕩}1⊑𝕩;
    "dfn strlist" 𝕊 𝕩:
        (•BQN fnsImport∾⊑𝕩){𝕎𝕩}1↓𝕩
}

{
    type ←⊑𝕩
    args ←1↓𝕩
    
    {
        ∨´2=⥊ •Type¨𝕩 ? 
            •Out 𝕩;
            •Show 𝕩
    } type Main args 

}⍟{⟨⟩≢𝕩} •args

fnsImport⇐"fns←•Import """∾•path∾"/fns.bqn"","

f←•Import "fns.bqn"

Main ←{
    fn 𝕊 args:
        repl←•ReBQN {repl⇐"strict",system⇐⟨f⟩}
        func←Repl fn
        Func{1=≠𝕩?𝔽⊑𝕩;"Function got more than 2 arguments"!2=≠𝕩?𝔽´⌽𝕩}⌾f.mediaryLang.Handler args
}

EvalFn←{
    fn ←⊑𝕩
    args ←1↓𝕩

    f.ToPyTuple fn Main args 
}

# •Show EvalFn "{2/𝕩}"‿"cnn"‿"a"‿"1"‿"2" 

•Out EvalFn⍟(⟨⟩⊸≢) •args
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

•Out EvalFn⍟(⟨⟩⊸≢) •args
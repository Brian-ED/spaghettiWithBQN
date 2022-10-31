f←•Import "fns.bqn"

Main ←{
  fn 𝕊 args:
    repl←•ReBQN {repl⇐"strict",system⇐⟨f⟩}
    func←Repl fn
    {
      𝕊⟨arg1⟩:
        f.Print Func arg1;
      𝕊arg1‿arg2:
        arg2 Func arg1;
      !"Function got more than 2 arguments"
    }⌾(f.IntoMediary⁼) args
}

EvalFn←{
  fn ←⊑𝕩
  args ←1↓𝕩

  f.ToPyTuple fn Main args 
}

•Out EvalFn⍟(⟨⟩⊸≢) •args
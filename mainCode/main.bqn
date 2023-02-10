f←•Import "fns.bqn"

Main ←{
  fn 𝕊 args:
    repl←•ReBQN {repl⇐"strict",system⇐⟨⟨"f",f⟩⟩}
    func←Repl fn
    {
      𝕊⟨a⟩:
        Func a;
      𝕊a‿b:
        b Func a;
      !"Function got invalid amount of arguments"
    }⌾(f.IntoMediary⁼) args
}

EvalFn←{
  fn ←⊑𝕩
  args ←1↓𝕩

  f.ToPyTuple fn Main args 
}
•Out∘EvalFn⍟(⟨⟩⊸≢)•args
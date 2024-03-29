Print ⇐⊢⊣  (•path∾"/out.txt") •FChars •Repr
IsString ⇐(1==)◶⟨0⋄∧´2=•Type¨⟩
ToPyTuple ⇐{«∾1⌽¨""","""⊸∾⟜∾¨"\"""⊸(⊑⊐)◶"\\"‿"\"""‿⥊¨¨𝕩}
Split ⇐(⊢-˜+`×¬)∘=⊔⊢

NN ← (>⟜«0⊸≤) / 0(0⊸≤××⟜10⊸+)`⊢

ReplaceAll ⇐ { ⟨old,new⟩ 𝕊 str:
  !new≠⊸≡l←≠old
  "ReplaceAll: Can't replace empty" ! ∧´0<≠¨old
  match ← 1-˜ (l+1)|⌊´ (↕⊸-l) × old (1<≠∘⊣)◶⟨⊑⊸=,≠∘⊢↑⍷⟩¨ <str
  cont ← (-⟜1⌈≤⟜1×⊢)` match ⊏ (≠¨old)∾0
  keep ← ⋈⟜(⊏⟜str) / 0=cont
  insert ← (new⊏˜⊏⟜match)⊸(≠¨⊸/⋈∾∘⊣) / (0⊸<∧»⊸≤) cont
  ⍋⊸⊏´ keep ∾¨ insert
}

# General numbers recognize digits and eE.¯-π∞ (mild extension of BQN) by Marshall
# Modified ToNums from Marshals string lib.
# Now works on True, False, and nans from python
ToNums ⇐ ({
  T←⌈`× ⋄ I1T←(1+↕∘≠)⊸T
  cd←≠dig←"π∞N"∾˜'0'+↕10 ⋄ val←π‿1‿1‿¯1∾˜↕10 # ∞ as 1 to avoid ∞×0
  e‿d‿n‿p‿i‿nan←"e.¯π∞N"=<𝕩 ⋄ e‿n∨↩"E-"=<𝕩
  m←d∨cd>j←dig⊐𝕩
  s←d∨c←e∨z←(∧`⌾⌽<»⊸<)zz←¬e∨n∨m
  "dubble spaces dissalowed"!¬∨´"  "⍷𝕩
  "Negative sign in the middle of a number"! ∧´n≤1»c
  "Portion of a number is empty"! ∧´¬(1«s)∧n∨s
  "Ill-formed decimal or exponent use"! ∧´(0⊸=∨»⊸<)s/d+2×e
  "π and ∞ must occur alone"! ∧´(p∨i)≤1(»∧(p∧«e)∨«)zz∨n>»e
  f←(17≥¬(⊢-T)+`)⊸∧g←(«≤(d<j≠0)>○I1T¬)⊸∧m   # No leading 0s; max 17 digits
  vs←1‿¯1⊏˜(r←>⟜»m)/»n                      # Negate if ¯
  v←vs×NN val⊏˜d¬⊸/j⌈cd×¬f                  # Numeric values—mantissas and exponents
  vm←c/○(1⌾⊑)z                              # Mask of mantissas in v
  dp←vm/f(--»⊸-(<×⊢)⊏⟜(I1T«d)⊸-)○(/>⟜«)g    # Decimal position
  q←10⋆|ee←dp-˜vm/«v×¬vm                    # Power of 10
  q÷˜⌾((0>ee)⊸/)q×⌾((0<ee)⊸/)vm/v×⟨1,∞,0÷0⟩⊏˜⌈´(1+↕∘≠)⊸×r⊸/¨i‿nan # Correct ∞ then ×10⋆ee
}⟨"True"‿"False"‿"inf"‿"nan"
  "1"   ‿"0"    ‿"∞"  ‿"N"
⟩ReplaceAll⊢)⍟(⟨⟩⊸≢)

ExtractTypes ←{
  IsString 𝕩? "s";
  0=•Type𝕩?
    ""∾´("l"⊸∾⍟(0=≠)'l'»«""∾´' '∾¨•Repr¨≢𝕩)∾""∾´𝕊¨⥊𝕩;
  6=•Type𝕩?"F";
  "ncf"⊑˜2⌊¯1+•Type 𝕩
}

Crunch←{
  x←⟨⟩
  IsString◶{
    x∾↩⥊¨∾∘("¯∞N"⊸(⊑⊐)◶"-"‿"inf"‿"n"‿⥊¨•Repr)⍟(2≠•Type)¨⥊𝕩
  }‿{
    x∾↩<𝕩
  }⚇1𝕩
  x
}

IntoMediary ⇐{
  𝕊: (ExtractTypes <⊸∾ Crunch) 𝕩;
  𝕊⁼:
    types ←⊑𝕩
    args ←1↓𝕩
    
    typesInShape←⊑""≡⟜'l'◶⟨
      ∾˜
      {-+´𝕩∊' '∾'0'+↕10}(⌽∘ToNums∘↑(×´⊸↓ ⌽⊸∾ <∘⥊)⌽∘↓)⊢
    ⟩´types

    args GroupTypes typesInShape
}
NewPyFunc⇐{𝕊fName:
  {comm𝕊inp: fName comm.PyFunc inp}
}
GroupTypes←{args𝕊typesInShape:
  x←𝕨
  F←{𝕊:(x⌽˜↩1)⊢⊑x}
  {(F@){𝕏𝕨}(⊑ToNums)‿⊢‿⊑‿•BQN‿NewPyFunc⊑˜⊑"nscfF"⊐𝕩}⚇0 𝕩
}

CreateComm⇐{
  commPath⇐@≡◶⊢‿"Default"𝕩
  (IsString commPath)        !˜"Only strings as name of communication allowed"
  (∧´commPath∊"_"∾⥊"aA"+⌜↕26)!˜"only alphabetical characters and spaces as name of communication allowed"
  commPath∾˜↩"comm/"
  •file.CreateDir⍟(¬•file.Exists) commPath

  # MsgExists⇐{𝕊:"TODO"}

  CleanMsgs ⇐ (•file.Remove¨<∘∾⟜'/'∾¨•file.List)∘commPath

  SendMsg ⇐ {
    𝕊⁼:GetMsg 1;
    path←commPath∾"/msgFromBQN"∾(•Repr≠•file.List commPath)∾".txt"
    path •FChars ToPyTuple IntoMediary 𝕩
  }

  noMsgError←"No msg found. Please ⎊ if expected, or 'GetMsg 1' to wait for msg"
  GetMsg ⇐{
    FindFile←"msgFromPy"⊸(⊣≡≠⊸↑)¨•file.List
    m←FindFile∘commPath •_while_{•Delay 0.2⋄¬∨´𝕩}⍟(1≡𝕩) FindFile commPath
    noMsgError!∨´m
    file←⊑∧m/•file.List commPath
    {a ← IntoMediary⁼ •BQN •FChars 𝕩 ⋄ •file.Remove𝕩 ⋄ a} commPath∾'/'∾file
  }

  # TODO add .run so you can use python function in bqn
  PyFunc ⇐{
    funcName𝕊inp:
    !IsString 𝕩
    "applyPyFunc" SendMsg funcName⊸⋈
  }
}
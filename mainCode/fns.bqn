_While_ ⇐{𝔽⍟𝔾∘𝔽_𝕣_𝔾∘𝔽⍟𝔾𝕩}
ToInt ⇐10⊸×⊸+˜´∘⌽-⟜'0'
StartsWith ⇐ ≤○≠◶⟨0⋄⊣≡≠⊸↑⟩˜
Print ⇐⊢⊣  (•path∾"/../out.txt") •FChars •Repr
IsString ⇐(1==)◶⟨0⋄∧´2=•Type¨⟩
ToPyTuple ⇐{'['∾']'«∾1⌽¨""","""⊸∾⟜∾¨"\"""⊸(⊑⊐)◶"\\"‿"\"""‿⥊¨¨𝕩}
PrefixedInteger ←⊢(⊢∾⟜ToInt 1↓↑˜)1+⟜(+´∧`)1↓∊⟜('0'+↕10)
Split←(⊢-˜+`×¬)∘=⊔⊢
S←•Show
ToInts←ToInt¨' 'Split⊢

# TODO add .run so you can use python function in bqn
PyFunc ⇐{
  𝕊funcName:
  !IsString 𝕩
  "applyPyFunc" comm.SendMsg funcName⊸⋈
}

x‿y←PyFunc¨ "hello"‿"hi"
•Show x‿y

ExtractTypes ←{
  IsString 𝕩? 's';
  0=•Type 𝕩?
    ∾´('l'»«""∾´' '∾¨•Repr¨≢𝕩)∾∾´𝕊¨⥊𝕩;
  "ncf"⊑˜2⌊¯1+•Type 𝕩
}

Crunch←{
  x←⟨⟩
  IsString◶{
    x∾↩•Repr⍟(2≠•Type)¨⥊𝕩
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
    
    typesInShape←⊑⟨⟩≡⟜'l'◶⟨
      ∾˜
      {-+´𝕩∊' '∾'0'+↕10}(ToInts∘↑(⌽<∘⥊∾×´⊸↓)⌽∘↓)⊢
    ⟩´types

    args GroupTypes typesInShape
}

GroupTypes←{args𝕊typesInShape:
  x←𝕨
  F←{𝕊:(x⌽˜↩1)⊢⊑x}

  {(F@){𝕏𝕨}ToInt‿⊢‿⊑‿•BQN‿ PyFunc⊑˜⊑"nscfF"⊐𝕩}⚇0 𝕩
}

{𝕊:
S S⌾IntoMediary S⟨"helllo"⋄⟨1⋄2⋄3⋄⟨'a'⋄"boo"⟩⋄4⟩⟩
}⍟1@ #testing on or off

FileExists←⊢⊣"Couldn't find python file to run"!•file.Exists

comm⇐{

  commPath⇐"comm/Default"
  •file.Exists◶⟨
    •file.CreateDir
    •file.Remove¨<∘∾⟜'/'∾¨•file.List
  ⟩commPath
  •SH "Python3" ⋈ FileExists𝕨

  SetID⇐{
    "Only strings as name of communication allowed"!IsString𝕩
    (∧´𝕩∊"_"∾⥊"aA"+⌜↕26)!˜"only alphabetical characters and spaces as name of communication allowed"
    commPath←"comm/"∾𝕩
  }

  MsgExists⇐{𝕊:"TODO"}

  SendMsg ⇐ {
    action𝕊msg:
      !action∊⟨"applyPyFunc"⟩
      path←commPath∾"/msgFromBQN"∾action∾(•Repr≠•file.List commPath)∾".txt"
      path •FChars ToPyTuple IntoMediary msg;
    𝕊msg:
      path←commPath∾"/msgFromBQN"∾(•Repr≠•file.List commPath)∾".txt"
      path •FChars ToPyTuple IntoMediary msg;
    𝕊⁼:
      GetMsg 1
  }

  noMsgError←"No msg found. Please ⎊ if expected, or 'GetMsg 1' to wait for msg"
  GetMsg ⇐{
    wait←1≡𝕩
    FindFile←"msgFromPy"⊸(⊣≡≠⊸↑)¨•file.List
    m←FindFile _while_{•Delay 0.2⋄¬∨´𝕩}⍟wait FindFile commPath
    noMsgError!∨´m
    file←⊑∧m/•file.List commPath
    (•file.Remove⊢IntoMediary⁼∘•FChars) file
  }
}
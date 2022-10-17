_While_ ⇐{𝔽⍟𝔾∘𝔽_𝕣_𝔾∘𝔽⍟𝔾𝕩}
ToInt ⇐10⊸×⊸+˜´∘⌽-⟜'0'
StartsWith ⇐ ≤○≠◶0‿(⊣≡≠⊸↑)˜
Print ⇐⊢⊣  (•path∾"/../out.txt") •FChars •Repr
IsString ⇐{1==𝕩?∧´2=•Type¨𝕩;0}
ToPyTuple ⇐{'['∾']'«∾1⌽¨""","""⊸∾⟜∾¨"\"""⊸(⊑⊐)◶"\\"‿"\"""‿⥊¨¨𝕩}
PrefixedInteger ←⊢(⊢∾⟜ToInt 1↓↑˜)1+⟜(+´∧`)1↓∊⟜('0'+↕10)

CollapseInts ←{
    # ⟨ 's' ⟨ 3 3 3 ⟩ 's' 's' ⟨ 2 ⟩ 'n' 'n' 'n' 'n' ⟩ ≡ CollapseInts "sl3 3 3ssl2nnnn"
    # TODO can be massively simplified
    𝕊 done‿types:
        'l'≡⊑types?
        lenOfArg‿listLen←PrefixedInteger types
        ⌽⌾(⊑⌽∘⊑){ 𝕊 done‿types:
            lenOfArg‿listLen←PrefixedInteger types
            ⟨listLen⊸∾⌾(⊑⌽)done ,lenOfArg↓types⟩
        } _While_ {' '≡⊑1⊑𝕩}⍟(0=⟜≠1⟜⊑) Print ⟨done∾⟨⟨listLen⟩⟩,lenOfArg↓types⟩;
    𝕊 done‿types:
        (1⊸↓⋈˜done∾⊑)types
}_While_(""≢⊑∘⌽)

# TODO add .run so you can use python function in bqn
PyFuncStruct⇐{
    repr⇐𝕩
}

GroupTypes←{
    𝕊 args‿done‿types:
        0≡•Type ⊑types?
            ⟨args
            done (<∘⥊∾×´⊸↓)˜ ⊑types
            1↓types⟩;

    𝕊 args‿done‿types:
        ⟨1↓args
        done ∾˜ args {𝕏𝕨}○⊑ ToInt‿<‿⊢‿•BQN‿ PyFuncStruct/˜"nscfF"=⊑types
        1↓types⟩
}_While_(""≢⊑∘⌽)

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

    intStrTypes ←⊑ CollapseInts ⟨⟩‿types

    >1⊑ GroupTypes ⌽¨args‿⟨⟩‿intStrTypes
}

{𝕊:
•Show •Show⌾IntoMediary •Show⟨"helllo",⟨1,2,3,⟨'a',"boo"⟩,4⟩⟩
}⍟0@ #testing on or off

FileExists←⊢⊣"Couldn't find python file to run"!•file.Exists

Communication⇐{
 ∧´𝕩∊"_"∾⥊"aA"+⌜↕26?

  commPath⇐"communication/"∾𝕩
  •file.Exists◶⟨
    •file.CreateDir
    •file.Remove¨<∘∾⟜'/'∾¨•file.List
  ⟩commPath
  •SH "Python3" ⋈ FileExists𝕨

  SendMsg ⇐ {
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
    m←FindFile _while_{•Delay 0.2,¬∨´𝕩}⍟wait FindFile commPath
    noMsgError!∨´m
    file←⊑∧m/•file.List commPath
    (•file.Remove⊢IntoMediary⁼∘•FChars) file
  }
}
Mean ⇐(+´÷≠)•BQN
Join ⇐∾´
_While_ ⇐{𝔽⍟𝔾∘𝔽_𝕣_𝔾∘𝔽⍟𝔾𝕩}
ToInt ⇐10⊸×⊸+˜´∘⌽-⟜'0'
StartsWith ⇐ ≤○≠◶0‿(⊣≡≠⊸↑)˜

mediaryLang ⇐{
    # 𝕩 ≡≡≡ types
    PrefixedInteger ⇐⊢(⊢∾⟜ToInt 1↓↑˜)1+⟜(+´∧`)1↓∊⟜('0'+↕10)

    pyEval ⇐<"notDefined"

    CollapseInts ⇐{
        # ⟨ 's' ⟨ 3 3 3 ⟩ 's' 's' ⟨ 2 ⟩ 'n' 'n' 'n' 'n' ⟩ ≡ CollapseInts "sl3 3 3ssl2nnnn"
        # TODO can be massively simplified
        𝕊 done‿types:
            'l'≡⊑types?
            lenOfArg‿listLen←PrefixedInteger types
            { 𝕊 done‿types:
                lenOfArg‿listLen←PrefixedInteger types
                ⟨(listLen⊸∾⌾(⊑⌽)done),lenOfArg↓types⟩
            } _While_ {' '≡⊑1⊑𝕩} ⟨done∾⟨⟨listLen⟩⟩,lenOfArg↓types⟩;

        𝕊 done‿types:
            (done∾⊑types)‿(1↓types)

    }_While_(""≢⊑∘⌽)

    GroupTypes⇐{
        𝕊 args‿done‿types:
            0≡•Type ⊑types?
                ⟨args
                done (<∘⥊∾×´⊸↓)˜ ⊑types
                1↓types⟩;

        𝕊 args‿done‿types:
            ⟨1↓args
            done ∾˜ args {𝕏𝕨}○⊑ ToInt‿<‿⊢‿•BQN‿ PyEval/˜"nscfF"=⊑types
            1↓types⟩

    }_While_(""≢⊑∘⌽)

    Handler ⇐{
        types ←⊑𝕩
        args ←1↓𝕩

        intStrTypes ←⊑ CollapseInts ⟨⟩‿types

        1⊑ GroupTypes ⌽¨args‿⟨⟩‿intStrTypes
    }
}

{𝕊:
•Show mediaryLang.Handler ⟨"l3l4 3ccccccccccccl3 2nnnnnnl5ccl3sl2nnnnn","t","h","i","s","i","s"," ","a","t","e","s","t","1","2","3","4","5","6","a","b","nested","3","2","1","2","3"⟩
}⍟0 0 #testing on or off
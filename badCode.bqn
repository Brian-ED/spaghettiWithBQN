MapTypeToArgs ⇐{
    𝕊 evaluated‿types‿args:
        'l'≡⊑types?
            listLen←fns.ToInt 1↓types↑˜lenOfArg←1++´∧`1↓types∊'0'+↕10
            (𝕊 ⊑∾1⊸⊑∾2⊸⊑) 𝕊⍟listLen ⟨⟩‿(lenOfArg↓types)‿args;

    𝕊 evaluated‿types‿args:
        's'≡⊑types?
            𝕊 (1↓types) args;
    
    𝕊 evaluated‿types‿args:
        'n'≡⊑types?
            fns.ToInt ⊑args
}
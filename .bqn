fns←•Import "/home/brian/personal/code/py/spaghettiWithBacon/fns.bqn"
MapTypeToArgs ⇐{
    𝕊 evaluated‿nesting‿types‿args:
        'l'≡⊑types?
            listLen←fns.ToInt 1↓types↑˜lenOfArg←1++´∧`1↓types∊'0'+↕10
            ⟨evaluated,listLen∾nesting,lenOfArg↓types,args⟩;

    𝕊 evaluated‿nesting‿types‿args:
        's'≡⊑types?
            ⟨(1↑args)⊸∾⌾(⊑⍟(≠nesting)) evaluated,nesting∾listLen,lenOfArg↓types,args⟩;

    𝕊 evaluated‿nesting‿types‿args:
        's'≡⊑types?;
        •Show ("test"⊸∾⌾⊑)⌾2⟨⟨⟩⟩

} fns._While_(⟨⟩⊸≢¨1⊸↓)
•Show MapTypeToArgs ⟨⟩‿⟨⟩‿"l3ssl2nnnn"‿⟨"aa","bb","cc","11","22","4","5"⟩
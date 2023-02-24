⟨CreateComm, IntoMediary⟩←•Import"fns.bqn"
comm←CreateComm@
# •Show comm.SendMsg⁼@
comm.CleanMsgs@

conds←[
    0 # comm.sendMsg
    0 # IntoMediary
    0 # IntoMediary⁼
]

testArrays←⟨
  # bottom list is the mediary representation of the top array  
  ⟨3‿4⥊"thisis atest",3‿2⥊(0÷0)‿∞‿¯∞‿4‿5‿6,⟨'a','b',⟨"nested",3‿2,1⟩,2,"sum"⟩⟩
  ⟨"l3l3 4ccccccccccccl3 2nnnnnnl5ccl3sl2nnnns","t","h","i","s","i","s"," ","a","t","e","s","t","nan","inf","-inf","4","5","6","a","b","nested","3","2","1","2","sum"⟩
⟩


{𝕏@}⚇0 conds/⟨
{𝕊: •Show comm.SendMsg "hellooo"}
{𝕊:
  !⟨"s"⋄"hellooo" ⟩≡IntoMediary "hellooo"
  !(1⊑testArrays)  ≡IntoMediary 0⊑testArrays
}
{𝕊: !(⊑testArrays)≡○•Repr IntoMediary⁼ 1⊑testArrays  # repr used because ≢˜0÷0, but ≡○•Reor˜0÷0
    !"abc"≡IntoMediary⁼ ⟨"s","abc"⟩
}
⟩

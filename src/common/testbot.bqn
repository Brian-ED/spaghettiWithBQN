⟨CreateComm, IntoMediary, Print⟩←•Import"fns.bqn"
comm←CreateComm"discBot"
# comm.CleanMsgs@
{𝕊:
    comm.SendMsg 1+comm.GetMsg 1
}•_while_ 1 @
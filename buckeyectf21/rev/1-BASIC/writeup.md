# Writeup

Download TI Connect and open `BASIC.8xp` in the program editor:

```
ClrHome
ClrList L₄
"F4X67ENQPK0{MTJRHL}O3G59UB-ZAWV8S2YI1CD"→Str2
{26,25,38,10,6,35,6,12,13,2,14,17,27,38,18,29,23,23,27,30,2,33,27,26,11,16,37,7,22,19}→L₄
Input "GUESS: ",Str7
If length(Str7)≠30:Then
Disp "WRONG"
Stop
End
For(I,1,30,1)
If sub(Str7,I,1)≠sub(Str2,L₄(I),1)
Then
Disp "WRONG"
Stop
End
End
Disp "CORRECT"
```

Solution: BUCKEYE{M4TH-CLA55-W4S-B0R1NG}

# Joshua Newberry

.globl intMax
.text

intMax:
    blt $a0, $a1, OneTop
    blt $a0, $a2, TwoTop
    move $v0, $a0
    jr $ra

OneTop:
    blt $a1, $a2, TwoBottom
OneBottom:
    move $v0, $a1
    jr $ra

TwoTop:
    blt $a2, $a1, OneBottom
TwoBottom:
    move $v0, $a2
    jr $ra
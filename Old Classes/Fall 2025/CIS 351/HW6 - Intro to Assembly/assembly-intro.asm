.globl monkeyTrouble sleepIn posNeg
.text

monkeyTrouble:
    beq $a0, $a1, Equals
    bne $a0, $a1, NotEquals

Equals:
    li $v0, 1
    jr $ra

NotEquals:
    li $v0, 0
    jr $ra

sleepIn:
    not $a0, $a0
    andi $a0, $a0, 1
    or $v0, $a0, $a1
    jr $ra

posNeg:
    slt $a0, $a0, $zero
    slt $a1, $a1, $zero
    beq $a2, 1, Negative
    bne $a2, 1, Regular

Negative:
    and $v0, $a0, $a1
    jr $ra

Regular:
    xor $v0, $a0, $a1
    jr $ra
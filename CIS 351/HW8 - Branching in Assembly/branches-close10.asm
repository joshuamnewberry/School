.globl close10
.text

close10:
    addi $t0, $a0, -10
    bgt $t0, $zero, Continue0
    neg $t0, $t0
Continue0:
    addi $t1, $a1, -10
    bgt $t1, $zero, Continue1
    neg $t1, $t1
Continue1:
    blt $t0, $t1, Zero
    blt $t1, $t0, One
    move $v0, $zero
    jr $ra
Zero:
    move $v0, $a0
    jr $ra
One:
    move $v0, $a1
    jr $ra
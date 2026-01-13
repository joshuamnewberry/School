.globl sum13
.text

sum13:
    move $v0, $0
    move $t0, $0
    li $t3, 13
    while_loop:
        bge $t0, $a1, end_while
        sll $t1, $t0, 2
        add $t1, $t1, $a0
        lw  $t2, 0($t1)
        bne $t2, $t3, end_if
        if:
            addi $t0, $t0, 2
            j while_loop
        end_if:
        add $v0, $v0, $t2
        addi $t0, $t0, 1
        j while_loop
    end_while:
    jr $ra
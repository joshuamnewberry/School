.globl max
.text

max:
    lw $v0, 0($a0)
    addi $t2, $0, 1
    for_loop:
        bge $t2, $a1, end_for
        sll $s2, $t2, 2
        add $s2, $s2, $a0
        lw $s1, 0($s2)
        ble $s1, $v0, end_if
        if:
            move $v0, $s1
        end_if:
        addi $t2, $t2, 1
        j for_loop
    end_for:
    jr $ra
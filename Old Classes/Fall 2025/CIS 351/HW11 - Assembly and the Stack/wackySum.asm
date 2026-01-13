.globl wackySum
.globl combineFour

wackySum:
    addi $sp, $sp, -12
    sw   $ra, 8($sp)
    sw   $s0, 4($sp)
    sw   $s1, 0($sp)

    move $s0, $a0
    li   $s1, 0

    wacky_loop:
        bgt  $s0, $a1, wacky_end

        move $t0, $s0
        addi $t1, $s0, 1
        sra  $t1, $t1, 1
        addi $t2, $s0, 2
        sra  $t2, $t2, 1

        addi $sp, $sp, -16
        sw   $a0, 0($sp)
        sw   $a1, 4($sp)
        sw   $a2, 8($sp)
        sw   $a3, 12($sp)

        move $a0, $t0
        move $a1, $t1
        move $a2, $t2
        addi $a3, $s0, 3

        jal  combineFour

        lw   $a0, 0($sp)
        lw   $a1, 4($sp)
        lw   $a2, 8($sp)
        lw   $a3, 12($sp)
        addi $sp, $sp, 16

        add  $s1, $s1, $v0
        add  $s0, $s0, $a2
        j    wacky_loop

    wacky_end:
    
    move $v0, $s1

    lw   $ra, 8($sp)
    lw   $s0, 4($sp)
    lw   $s1, 0($sp)
    addi $sp, $sp, 12
    jr   $ra

combineFour:
    addi $sp, $sp, -8
    sw   $ra, 4($sp)
    sw   $s0, 0($sp)

    add  $s0, $a0, $a1
    add  $s0, $s0, $a2
    add  $s0, $s0, $a3

    andi $t0, $s0, 1
    beq  $t0, $zero, combine_even

    sra  $v0, $s0, 1
    j    combine_end

combine_even:
    move $v0, $s0

combine_end:
    lw   $ra, 4($sp)
    lw   $s0, 0($sp)
    addi $sp, $sp, 8
    jr   $ra
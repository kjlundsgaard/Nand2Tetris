// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
// Pseudo code
// take memory at R0, loop through it R1 times, add value at R2 to it R1 times
// (set n to value at R1 and then subtract by 1, jump to end if 0)

    @R1
    D=M
    @n
    M=D // set variable n to value of memory 1

    @R2
    M=0 // initialize product to 0

(LOOP)
    @R0
    D=M // get value at memory address 0

    @R2
    M=D+M // increment address 2 by value at address 0

    @n
    M=M-1
    D=M
    @END
    D;JEQ // go to end if n is 0

    @LOOP
    0;JMP // go to LOOP

(END)
    @END
    0;JMP // infinite loop to end program

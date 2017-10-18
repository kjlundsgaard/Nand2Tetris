// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(LOOP)
    @KBD
    D=A
    @max
    M=D
    @SCREEN
    D=A
    @R0
    M=D //PUT SCREEN START LOCATION IN RAM0

(CHECK_KEY)
    @KBD
    D=M
    @FILL_LOOP
    D;JGT
    @ERASE_LOOP
    D;JEQ

(FILL_LOOP)
    @R0
    A=M //GET ADRESS OF SCREEN PIXEL TO FILL
    M=-1 //FILL IT WITH BLACK

    @R0
    MD=M+1   //INC TO NEXT PIXEL
    @max
    D=M-D   //KBD-SCREEN set D to kbd index minus current index

    @FILL_LOOP
    D;JGT   //IF A=0 (at end of screen idx) EXIT AS THE WHOLE SCREEN IS BLACK

    @LOOP
    0;JMP // infinite loop

(ERASE_LOOP)
    @R0
    A=M //GET ADRESS OF SCREEN PIXEL TO FILL
    M=0 //FILL IT WITH WHITE

    @R0
    MD=M+1   //INC TO NEXT PIXEL
    @max
    D=M-D   //KBD-SCREEN set D to kbd index minus current index

    @ERASE_LOOP
    D;JGT   //IF A=0 (at end of screen idx) EXIT AS THE WHOLE SCREEN IS WHITE

    @LOOP
    0;JMP // infinite loop
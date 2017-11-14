//push argument 1
                @ARG
                D=M
                @1
                A=D+A
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
//pop pointer 1
                @3
                D=A
                @1
                D=D+A
                @R13
                M=D
                @SP
                A=M-1
                D=M
                @R13
                A=M
                M=D
                @SP
                M=M-1
//push constant 0
                @0
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//pop that 0
                @THAT
                D=M
                @0
                D=D+A
                @R13
                M=D
                @SP
                A=M-1
                D=M
                @R13
                A=M
                M=D
                @SP
                M=M-1
//push constant 1
                @1
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//pop that 1
                @THAT
                D=M
                @1
                D=D+A
                @R13
                M=D
                @SP
                A=M-1
                D=M
                @R13
                A=M
                M=D
                @SP
                M=M-1
//push argument 0
                @ARG
                D=M
                @0
                A=D+A
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
//push constant 2
                @2
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//sub
                @SP
                D=M
                A=D-1
                D=M
                A=A-1
                M=M-D
                @SP
                M=M-1
//pop argument 0
                @ARG
                D=M
                @0
                D=D+A
                @R13
                M=D
                @SP
                A=M-1
                D=M
                @R13
                A=M
                M=D
                @SP
                M=M-1
// label
            (FibonacciSeries$MAIN_LOOP_START)
        
//push argument 0
                @ARG
                D=M
                @0
                A=D+A
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
 // if-goto label
            @SP
            A=M-1
            D=M
            @SP
            M=M-1
            @FibonacciSeries$COMPUTE_ELEMENT
            D;JNE
        
 // goto label
            @FibonacciSeries$END_PROGRAM
            0;JEQ
        
// label
            (FibonacciSeries$COMPUTE_ELEMENT)
        
//push that 0
                @THAT
                D=M
                @0
                A=D+A
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
//push that 1
                @THAT
                D=M
                @1
                A=D+A
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
//add
                @SP
                D=M
                A=D-1
                D=M
                A=A-1
                M=D+M
                @SP
                M=M-1
//pop that 2
                @THAT
                D=M
                @2
                D=D+A
                @R13
                M=D
                @SP
                A=M-1
                D=M
                @R13
                A=M
                M=D
                @SP
                M=M-1
//push pointer 1
                @3
                D=A
                @1
                A=D+A
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
//push constant 1
                @1
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//add
                @SP
                D=M
                A=D-1
                D=M
                A=A-1
                M=D+M
                @SP
                M=M-1
//pop pointer 1
                @3
                D=A
                @1
                D=D+A
                @R13
                M=D
                @SP
                A=M-1
                D=M
                @R13
                A=M
                M=D
                @SP
                M=M-1
//push argument 0
                @ARG
                D=M
                @0
                A=D+A
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
//push constant 1
                @1
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//sub
                @SP
                D=M
                A=D-1
                D=M
                A=A-1
                M=M-D
                @SP
                M=M-1
//pop argument 0
                @ARG
                D=M
                @0
                D=D+A
                @R13
                M=D
                @SP
                A=M-1
                D=M
                @R13
                A=M
                M=D
                @SP
                M=M-1
 // goto label
            @FibonacciSeries$MAIN_LOOP_START
            0;JEQ
        
// label
            (FibonacciSeries$END_PROGRAM)
        
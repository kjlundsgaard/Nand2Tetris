// function SimpleFunction.test 2
        (SimpleFunction.test)
            @2
            D=A
            @SimpleFunction.test.END_LOOP
            D;JLE
            (SimpleFunction.test.initloop)
            @SP
            A=M
            M=0
            @SP
            M=M+1
            D=D-1
            @SimpleFunction.test.initloop
            D;JGT
            (SimpleFunction.test.END_LOOP)
        
//push local 0
                @LCL
                D=M
                @0
                A=D+A
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
//push local 1
                @LCL
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
//not
                @SP
                D=M
                A=D-1
                M=!M
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
//add
                @SP
                D=M
                A=D-1
                D=M
                A=A-1
                M=D+M
                @SP
                M=M-1
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
//sub
                @SP
                D=M
                A=D-1
                D=M
                A=A-1
                M=M-D
                @SP
                M=M-1
 // return
            // frame = LCL
            @LCL
            D=M
            @FRAME
            M=D
            // retAddr = *(frame-5)
            @5
            D=A
            @FRAME
            D=M-D
            A=D
            D=M
            @RET
            M=D
            // *ARG = pop
            @SP
            A=M-1
            D=M
            @ARG
            A=M
            M=D
            // SP = ARG + 1
            @ARG
            D=M+1
            @SP
            M=D
            // THAT = *(frame-1)
            @FRAME
            D=M
            @1
            A=D-A
            D=M
            @THAT
            M=D
            // THIS = *(frame-2)
            @FRAME
            D=M
            @2
            A=D-A
            D=M
            @THIS
            M=D
            // ARG = *(frame-3)
            @FRAME
            D=M
            @3
            A=D-A
            D=M
            @ARG
            M=D
            // LCL = *(frame-4)
            @FRAME
            D=M
            @4
            A=D-A
            D=M
            @LCL
            M=D
            @RET
            A=M
            0;JMP
        
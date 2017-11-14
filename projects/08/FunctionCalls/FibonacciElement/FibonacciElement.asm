
            @256
            D=A
            @SP
            M=D
            @RET_Sys.init
            D=A
            @SP
            A=M
            M=D
            @SP
            M=M+1
            @LCL
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            @ARG
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            // push THIS
            @THIS
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            // push THAT
            @THAT
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            // ARG = SP - {num_args} - 5
            @SP
            D=M
            @5
            D=D-A
            @ARG
            M=D
            // LCL = SP
            @SP
            D=M
            @LCL
            M=D
            @Sys.init
            0;JMP
            (RET_Sys.init)
        
// function Main.fibonacci 0
        (Main.fibonacci)
            @0
            D=A
            @Main.fibonacci.END_LOOP
            D;JLE
            (Main.fibonacci.initloop)
            @SP
            A=M
            M=0
            @SP
            M=M+1
            D=D-1
            @Main.fibonacci.initloop
            D;JGT
            (Main.fibonacci.END_LOOP)
        
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
//lt
                @R14
                M=-1 //-1 is 0xfffffff which is true
                @SP
                D=M
                A=D-1
                D=M
                A=A-1
                //D is zero if x and y are equal
                D=M-D
                //decrement stack point
                @SP
                M=M-1
                //jump if values are equal, greaterthan, or lessthan
                @Main.jmp0
                D;JLT
                //if we're here, the jump condition failed, so set R14 to false
                @R14
                M=0
            (Main.jmp0)
                //push R14 onto stack
                @R14
                D=M
                @SP
                A=M-1
                M=D
                
 // if-goto label
            @SP
            A=M-1
            D=M
            @SP
            M=M-1
            @Main$IF_TRUE
            D;JNE
        
 // goto label
            @Main$IF_FALSE
            0;JEQ
        
// label
            (Main$IF_TRUE)
        
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
            @RET.0
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
            @RET.0
            A=M
            0;JMP
        
// label
            (Main$IF_FALSE)
        
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
// call Main.fibonacci 1
            //push returnAddress
            @Main.fibonacci.returnAddress.1
            D=A
            @SP
            A=M
            M=D
            @SP
            M=M+1
            // push LCL
            @LCL
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            // push ARG
            @ARG
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            // push THIS
            @THIS
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            // push THAT
            @THAT
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            // ARG = SP - 1 - 5
            @SP
            D=M
            @5
            D=D-A
            @1
            D=D-A
            @ARG
            M=D
            // LCL = SP
            @SP
            D=M
            @LCL
            M=D
            // goto Main.fibonacci
            @Main.fibonacci
            0;JMP
        (Main.fibonacci.returnAddress.1)
        
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
// call Main.fibonacci 1
            //push returnAddress
            @Main.fibonacci.returnAddress.2
            D=A
            @SP
            A=M
            M=D
            @SP
            M=M+1
            // push LCL
            @LCL
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            // push ARG
            @ARG
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            // push THIS
            @THIS
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            // push THAT
            @THAT
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            // ARG = SP - 1 - 5
            @SP
            D=M
            @5
            D=D-A
            @1
            D=D-A
            @ARG
            M=D
            // LCL = SP
            @SP
            D=M
            @LCL
            M=D
            // goto Main.fibonacci
            @Main.fibonacci
            0;JMP
        (Main.fibonacci.returnAddress.2)
        
//add
                @SP
                D=M
                A=D-1
                D=M
                A=A-1
                M=D+M
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
            @RET.3
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
            @RET.3
            A=M
            0;JMP
        
// function Sys.init 0
        (Sys.init)
            @0
            D=A
            @Sys.init.END_LOOP
            D;JLE
            (Sys.init.initloop)
            @SP
            A=M
            M=0
            @SP
            M=M+1
            D=D-1
            @Sys.init.initloop
            D;JGT
            (Sys.init.END_LOOP)
        
//push constant 4
                @4
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
// call Main.fibonacci 1
            //push returnAddress
            @Main.fibonacci.returnAddress.0
            D=A
            @SP
            A=M
            M=D
            @SP
            M=M+1
            // push LCL
            @LCL
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            // push ARG
            @ARG
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            // push THIS
            @THIS
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            // push THAT
            @THAT
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            // ARG = SP - 1 - 5
            @SP
            D=M
            @5
            D=D-A
            @1
            D=D-A
            @ARG
            M=D
            // LCL = SP
            @SP
            D=M
            @LCL
            M=D
            // goto Main.fibonacci
            @Main.fibonacci
            0;JMP
        (Main.fibonacci.returnAddress.0)
        
// label
            (Sys$WHILE)
        
 // goto label
            @Sys$WHILE
            0;JEQ
        
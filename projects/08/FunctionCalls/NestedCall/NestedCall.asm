
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
        
//push constant 4000
                @4000
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//pop pointer 0
                @3
                D=A
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
//push constant 5000
                @5000
                D=A
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
// call Sys.main 0
            //push returnAddress
            @Sys.main.returnAddress.0
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
            // ARG = SP - 0 - 5
            @SP
            D=M
            @5
            D=D-A
            @0
            D=D-A
            @ARG
            M=D
            // LCL = SP
            @SP
            D=M
            @LCL
            M=D
            // goto Sys.main
            @Sys.main
            0;JMP
        (Sys.main.returnAddress.0)
        
//pop temp 1
                @5
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
// label
            (Sys$LOOP)
        
 // goto label
            @Sys$LOOP
            0;JEQ
        
// function Sys.main 5
        (Sys.main)
            @5
            D=A
            @Sys.main.END_LOOP
            D;JLE
            (Sys.main.initloop)
            @SP
            A=M
            M=0
            @SP
            M=M+1
            D=D-1
            @Sys.main.initloop
            D;JGT
            (Sys.main.END_LOOP)
        
//push constant 4001
                @4001
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//pop pointer 0
                @3
                D=A
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
//push constant 5001
                @5001
                D=A
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
//push constant 200
                @200
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//pop local 1
                @LCL
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
//push constant 40
                @40
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//pop local 2
                @LCL
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
//push constant 6
                @6
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//pop local 3
                @LCL
                D=M
                @3
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
//push constant 123
                @123
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
// call Sys.add12 1
            //push returnAddress
            @Sys.add12.returnAddress.1
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
            // goto Sys.add12
            @Sys.add12
            0;JMP
        (Sys.add12.returnAddress.1)
        
//pop temp 0
                @5
                D=A
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
//push local 2
                @LCL
                D=M
                @2
                A=D+A
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
//push local 3
                @LCL
                D=M
                @3
                A=D+A
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
//push local 4
                @LCL
                D=M
                @4
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
//add
                @SP
                D=M
                A=D-1
                D=M
                A=A-1
                M=D+M
                @SP
                M=M-1
//add
                @SP
                D=M
                A=D-1
                D=M
                A=A-1
                M=D+M
                @SP
                M=M-1
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
            @RET.2
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
            @RET.2
            A=M
            0;JMP
        
// function Sys.add12 0
        (Sys.add12)
            @0
            D=A
            @Sys.add12.END_LOOP
            D;JLE
            (Sys.add12.initloop)
            @SP
            A=M
            M=0
            @SP
            M=M+1
            D=D-1
            @Sys.add12.initloop
            D;JGT
            (Sys.add12.END_LOOP)
        
//push constant 4002
                @4002
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//pop pointer 0
                @3
                D=A
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
//push constant 5002
                @5002
                D=A
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
//push constant 12
                @12
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
        
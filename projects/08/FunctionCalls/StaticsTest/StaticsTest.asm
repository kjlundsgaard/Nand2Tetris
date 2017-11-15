
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
        
// function Class1.set 0
        (Class1.set)
            @0
            D=A
            @Class1.set.END_LOOP
            D;JLE
            (Class1.set.initloop)
            @SP
            A=M
            M=0
            @SP
            M=M+1
            D=D-1
            @Class1.set.initloop
            D;JGT
            (Class1.set.END_LOOP)
        
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
//pop static 0
                @SP
                A=M-1
                D=M
                @Class1.0
                M=D
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
//pop static 1
                @SP
                A=M-1
                D=M
                @Class1.1
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
        
// function Class1.get 0
        (Class1.get)
            @0
            D=A
            @Class1.get.END_LOOP
            D;JLE
            (Class1.get.initloop)
            @SP
            A=M
            M=0
            @SP
            M=M+1
            D=D-1
            @Class1.get.initloop
            D;JGT
            (Class1.get.END_LOOP)
        
//push static 0
                @Class1.0
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
//push static 1
                @Class1.1
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
            @RET.1
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
            @RET.1
            A=M
            0;JMP
        
// function Class2.set 0
        (Class2.set)
            @0
            D=A
            @Class2.set.END_LOOP
            D;JLE
            (Class2.set.initloop)
            @SP
            A=M
            M=0
            @SP
            M=M+1
            D=D-1
            @Class2.set.initloop
            D;JGT
            (Class2.set.END_LOOP)
        
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
//pop static 0
                @SP
                A=M-1
                D=M
                @Class2.0
                M=D
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
//pop static 1
                @SP
                A=M-1
                D=M
                @Class2.1
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
        
// function Class2.get 0
        (Class2.get)
            @0
            D=A
            @Class2.get.END_LOOP
            D;JLE
            (Class2.get.initloop)
            @SP
            A=M
            M=0
            @SP
            M=M+1
            D=D-1
            @Class2.get.initloop
            D;JGT
            (Class2.get.END_LOOP)
        
//push static 0
                @Class2.0
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
//push static 1
                @Class2.1
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
            @RET.1
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
            @RET.1
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
        
//push constant 6
                @6
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//push constant 8
                @8
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
// call Class1.set 2
            //push returnAddress
            @Class1.set.returnAddress.0
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
            // ARG = SP - 2 - 5
            @SP
            D=M
            @5
            D=D-A
            @2
            D=D-A
            @ARG
            M=D
            // LCL = SP
            @SP
            D=M
            @LCL
            M=D
            // goto Class1.set
            @Class1.set
            0;JMP
        (Class1.set.returnAddress.0)
        
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
//push constant 23
                @23
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//push constant 15
                @15
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
// call Class2.set 2
            //push returnAddress
            @Class2.set.returnAddress.1
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
            // ARG = SP - 2 - 5
            @SP
            D=M
            @5
            D=D-A
            @2
            D=D-A
            @ARG
            M=D
            // LCL = SP
            @SP
            D=M
            @LCL
            M=D
            // goto Class2.set
            @Class2.set
            0;JMP
        (Class2.set.returnAddress.1)
        
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
// call Class1.get 0
            //push returnAddress
            @Class1.get.returnAddress.2
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
            // goto Class1.get
            @Class1.get
            0;JMP
        (Class1.get.returnAddress.2)
        
// call Class2.get 0
            //push returnAddress
            @Class2.get.returnAddress.3
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
            // goto Class2.get
            @Class2.get
            0;JMP
        (Class2.get.returnAddress.3)
        
// label
            (Sys$WHILE)
        
 // goto label
            @Sys$WHILE
            0;JEQ
        
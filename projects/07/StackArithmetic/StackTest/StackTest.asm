//push constant 17
                @17
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//push constant 17
                @17
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//eq
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
                @StackTest.jmp0
                D;JEQ
                //if we're here, the jump condition failed, so set R14 to false
                @R14
                M=0
            (StackTest.jmp0)
                //push R14 onto stack
                @R14
                D=M
                @SP
                A=M-1
                M=D
                
//push constant 17
                @17
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//push constant 16
                @16
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//eq
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
                @StackTest.jmp1
                D;JEQ
                //if we're here, the jump condition failed, so set R14 to false
                @R14
                M=0
            (StackTest.jmp1)
                //push R14 onto stack
                @R14
                D=M
                @SP
                A=M-1
                M=D
                
//push constant 16
                @16
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//push constant 17
                @17
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//eq
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
                @StackTest.jmp2
                D;JEQ
                //if we're here, the jump condition failed, so set R14 to false
                @R14
                M=0
            (StackTest.jmp2)
                //push R14 onto stack
                @R14
                D=M
                @SP
                A=M-1
                M=D
                
//push constant 892
                @892
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//push constant 891
                @891
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
                @StackTest.jmp3
                D;JLT
                //if we're here, the jump condition failed, so set R14 to false
                @R14
                M=0
            (StackTest.jmp3)
                //push R14 onto stack
                @R14
                D=M
                @SP
                A=M-1
                M=D
                
//push constant 891
                @891
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//push constant 892
                @892
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
                @StackTest.jmp4
                D;JLT
                //if we're here, the jump condition failed, so set R14 to false
                @R14
                M=0
            (StackTest.jmp4)
                //push R14 onto stack
                @R14
                D=M
                @SP
                A=M-1
                M=D
                
//push constant 891
                @891
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//push constant 891
                @891
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
                @StackTest.jmp5
                D;JLT
                //if we're here, the jump condition failed, so set R14 to false
                @R14
                M=0
            (StackTest.jmp5)
                //push R14 onto stack
                @R14
                D=M
                @SP
                A=M-1
                M=D
                
//push constant 32767
                @32767
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//push constant 32766
                @32766
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//gt
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
                @StackTest.jmp6
                D;JGT
                //if we're here, the jump condition failed, so set R14 to false
                @R14
                M=0
            (StackTest.jmp6)
                //push R14 onto stack
                @R14
                D=M
                @SP
                A=M-1
                M=D
                
//push constant 32766
                @32766
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//push constant 32767
                @32767
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//gt
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
                @StackTest.jmp7
                D;JGT
                //if we're here, the jump condition failed, so set R14 to false
                @R14
                M=0
            (StackTest.jmp7)
                //push R14 onto stack
                @R14
                D=M
                @SP
                A=M-1
                M=D
                
//push constant 32766
                @32766
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//push constant 32766
                @32766
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//gt
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
                @StackTest.jmp8
                D;JGT
                //if we're here, the jump condition failed, so set R14 to false
                @R14
                M=0
            (StackTest.jmp8)
                //push R14 onto stack
                @R14
                D=M
                @SP
                A=M-1
                M=D
                
//push constant 57
                @57
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//push constant 31
                @31
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//push constant 53
                @53
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
//push constant 112
                @112
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
//neg
                @SP
                D=M
                A=D-1
                M=-M
//and
                @SP
                D=M
                A=D-1
                D=M
                A=A-1
                M=M&D
                @SP
                M=M-1
//push constant 82
                @82
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
//or
                @SP
                D=M
                A=D-1
                D=M
                A=A-1
                M=M|D
                @SP
                M=M-1
//not
                @SP
                D=M
                A=D-1
                M=!M

            (END)
            @END
            0;JMP   //FOREVER LOOP
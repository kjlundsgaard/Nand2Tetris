//push constant 7
                @7
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
//add
                @SP
                D=M
                A=D-1
                D=M
                A=A-1
                M=D+M
                @SP
                M=M-1

            (END)
            @END
            0;JMP   //FOREVER LOOP
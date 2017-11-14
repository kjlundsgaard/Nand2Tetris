# Nand2Tetris

## Building a Modern Computer From First Principles
--------------------------------------------------
These are my completed projects for Nand2Tetris, which aims to build a computer starting with a Nand gate and working my way up to an operating system. So far I have completed the following:

1. Implemented basic chips using a hardware description language - Not, And, Or, Xor, Mux, DMux, Not16, And16, Or16, Mux16, Or8Way, Mux4Way16, Mux8Way16, DMux4Way, DMux8Way

2. Implemented a HalfAdder, FullAdder, Add16, Inc16, and ALU with status outputs (negative and zero) in HDL

3. Given a data flip flop, implemented a 1-bit register, 16-bit register, RAM8, RAM64, RAM512, RAM4K, RAM16K, and a Program Counter in HDL

4. Wrote a program that multiplies two integers as well as a program that fills all of a screen's pixels with black when a keyboard key is pressed, both written in an assembly language

5. Build CPU and RAM (including screen and keyboard memory) in HDL, and combine with ROM32K to build full Computer chip

6. Write an assembler that takes in a file written in the hack assembly language and outputs the file assembled into binary

7. Implement a VM Translator that takes in a directory with files or single file written in VM code and outputs a file with corresponding hack assembly commands

8. Allow VM Translator to take in a directory and call a Sys.init function as well as handle other function calls and outputs a single file in hack assembly

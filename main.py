#!/usr/bin/env python

from sys import argv
from subprocess import call
from subprocess import *
from assembler import *


def options():
    op1=check_output(["echo","FORMAT: \n \t python3 python_filename asm_filename [options]"], universal_newlines=True)
    print(op1)
    op2=check_output(["echo", "The options are:"], universal_newlines=True)
    print(op2)
    op3=check_output(["echo", "\t -s \t Display Symbol Table"], universal_newlines=True)
    print(op3)
    op4=check_output(["echo", "\t -l \t Display Literal Table"], universal_newlines=True)
    print(op4)
    op5=check_output(["echo", "\t -i \t Display Intermediate Code"], universal_newlines=True)
    print(op5)
    op6=check_output(["echo", "\t -lst \t Display lst Code"], universal_newlines=True)
    print(op6)
    op7=check_output(["echo", "\t -o \t Display object code"], universal_newlines=True)
    print(op7)
    
    
    
def disp_option(op):
    if op=='-s':
        call(["less","symbol.txt"])

    if op=='-l':
        call(["less","literal.txt"])

    if op=='-i':
        call(["less","inter_code.txt"])

    if op=='-lst':
        call(["less","lst_op.txt"])

    if op=='-o':
        call(["less","obj_op.txt"])

    

        
    
if __name__ == "__main__":
    a=argv[1]
    disp_option(a)
    options()
    exit()
        
    

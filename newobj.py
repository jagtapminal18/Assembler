def add_space(s):
    s1=[s[i:i+2] for i in range(0,len(s),2)]
    r=' '.join(s1)
    return r
def replace_x(s):
    for i in s:
        if(i=='x'):
            s=s.replace(i,'0')
    return s.upper()
def addr(s):
    cnt=0
    ls=['[',']','(',')']
    for i in s:
        if i not in ls:
            cnt+=1
        else:
            exit
        c=int(cnt)/2
    return int(c)           
            
def object_code(f1,f2,f3,f4,f5,f6):
    reg32=["eax","ebx","ecx","edx","ebp","esp","esi","edi"]#32bit register
    reg16=["ax","bx","cx","dx"]#16bit register
    reg8=["ah","al","bh","bl","ch","cl","dh","dl"]#8bit register
    repint=["rep","repe","repne","repz"]#rep instruction list
    jmpint=["je","jne","jg","jge","jl","jle","jz"]#jmp instn
    fn1=open(f1,"r")#add.asm
    fn2=open(f2,"r")#symbol.txt
    fn3=open(f3,"r")#literal.txt
    fn4=open(f4,"r")#mod.txt
    fn5=open(f5,"r")#inter_code.txt
    fn6=open(f6,"r")#opc.txt
    ln1=fn1.readline()
    ln2=fn2.read()
    ln3=fn3.read()
    ln4=fn4.read()
    ln5=fn5.read()
    ln6=fn6.read()
    ls1=ln1.split()
    ls2=ln2.split()
    ls3=ln3.split()
    ls4=ln4.split()
    ls5=ln5.split()
    ls6=ln6.split()
    l1=len(ls1)
    l2=len(ls2)
    l3=len(ls3)
    l4=len(ls4)
    l5=len(ls5)
    l6=len(ls6)
    fout=open("obj_op.txt","w")
    lcnt=0
    ls7=[]
    for ln1 in fn1:
        lcnt+=1
        #print(lcnt)
        ls1=ln1.split()
        l1=len(ls1)
        for i in range(l1):
            if(ls1[i]=="section"):
                if(ls1[i+1]==".data"):
                    add1=80840014
                    fout.write(str(add1)+"<__data_start>:"+"\n")
                if(ls1[i+1]==".bss"):
                    add2=80840024
                    fout.write(str(add2)+"<__bss_start>:"+"\n")
            if(ls1[i]=="dd"):
                for j in range(l2):
                    if ls1[i-1]==ls2[j]:
                        a=ls2[j+2]
                        #print(a)
                f=str(replace_x(hex(int(ls1[i+1])))).zfill(4)
                ls7.append(ls1[i-1])
                ls7.append(add1)
                fout.write("\t\t\t"+str(add1)+"\t"+str(add_space(f))+"\n")
                add1=add1+int(a)
            if(ls1[i]=="db"):
                f=str(replace_x(hex(10)+hex(0))).zfill(4)
                fout.write("\t\t\t"+str(add1)+"\t"+str(add_space(f))+"\n")
            if(ls1[i]=="resb"):
                c=0000
                f=str(c).zfill(4)
                a=ls1[i+1]
                fout.write("\t\t\t"+str(add2)+"\t"+str(add_space(f))+"\n")
                add2=add2+int(a)
            if(ls1[i]=="resd"):
                c=0000
                f=str(c).zfill(4)
                a=int(ls1[i+1])*4
                fout.write("\t\t\t"+str(add2)+"\t"+str(add_space(f))+"\n")
                add2=add2+int(a)            
            if(ls1[i]=="main:"):
                add=80840044
                fout.write(str(add)+"<main>:"+"\n")
            if(ls1[i]=="mov"):
                ls=ls1[i+1].split(",")
                #for mov reg32,mem
                if(ls[1].startswith("dword")): #mov reg32,mem
                    s=ls1[1].split("[")
                    #print(s)
                    ss=s[1].split("]")
                    #print(ss)
                    if(ls[0] in reg32 and ss[0] in ls2):
                        for j in range(len(ls7)):
                            if ss[0]==ls7[j]:
                                s1=ls7[j+1]
                                #print(s1)
                        for k in range(l5):
                            if str(lcnt)==ls5[k]:
                                p=ls5[k+2]
                               # print(p)
                        for l in range(l6):
                            if str(p)==ls6[l]:
                                p1=ls6[l+1]
                        f=p1+str(s1)[::-1]
                        #print(f)
                        fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                        add=add+addr(f)
                #mov reg16,mem
                if(ls[0] in reg16 and ls[1] in ls2):
                    for j in range(len(ls7)):
                        if ls[1]==ls7[j]:
                            s1=ls7[j+1]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+str(s1)[::-1]
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                #mov reg8,mem
                if(ls[0] in reg8 and ls[1] in ls2):
                    for j in range(len(ls7)):
                        if ls[1]==ls7[j]:
                            s1=ls7[j+1]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+str(s1)[::-1]
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                    #mov reg32,imm
                if(ls[0] in reg32 and ls[1] in ls3):
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            s1=ls3[j]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+s1.zfill(8)[::-1]
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                #for mov reg16,imm
                if(ls[0] in reg16 and ls[1] in ls3):
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            s1=ls3[j]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+s1.zfill(8)[::-1]
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                #for mov reg8,imm
                if(ls[0] in reg8 and ls[1] in ls3):
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            s1=ls3[j]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+s1.zfill(8)[::-1]
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                    #mov reg32,reg32
                if(ls[0] in reg32 and ls[1] in reg32):
                    for x in reg32:
                        if x==ls[0]:
                            r1=x
                    for y in reg32:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+s1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                #for mov reg16,reg16
                if(ls[0] in reg16 and ls[1] in reg16):
                    for x in reg16:
                        if x==ls[0]:
                            r1=x
                    for y in reg16:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+s1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                #for mov reg8,reg8
                if(ls[0] in reg8 and ls[1] in reg8):
                    for x in reg8:
                        if x==ls[0]:
                            r1=x
                    for y in reg8:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+s1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                    #for  add instruction
            if(ls1[i]=="add"):
                ls=ls1[i+1].split(",")    
                if(ls[0] in reg32 and ls[1] in reg32):
                    for x in reg32:
                        if x==ls[0]:
                            r1=x
                    for y in reg32:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+s1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                #for add reg16,reg16
                if(ls[0] in reg16 and ls[1] in reg16):
                    for x in reg16:
                        if x==ls[0]:
                            r1=x
                    for y in reg16:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+s1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                #for add reg8,reg8
                if(ls[0] in reg8 and ls[1] in reg8):
                    for x in reg8:
                        if x==ls[0]:
                            r1=x
                    for y in reg8:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+s1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                    #for add reg,imm
                if(ls[0] in reg32 and ls[1] in ls3):
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            s1=ls3[j]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+s1.zfill(8)[::-1]
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
       
                if(ls[0] in reg16 and ls[1] in ls3):
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            s1=ls3[j]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+s1.zfill(8)[::-1]
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
               
                if(ls[0] in reg16 and ls[1] in ls3):
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            s1=ls3[j]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+s1.zfill(8)[::-1]
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                    #for sub instruct
            if(ls1[i]=="sub"):
                ls=ls1[i+1].split(",")    
                if(ls[0] in reg32 and ls[1] in reg32):#sub reg,reg
                    for x in reg32:
                        if x==ls[0]:
                            r1=x
                    for y in reg32:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+s1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
        
                if(ls[0] in reg16 and ls[1] in reg16):
                    for x in reg16:
                        if x==ls[0]:
                            r1=x
                    for y in reg16:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+s1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
              
                if(ls[0] in reg8 and ls[1] in reg8):
                    for x in reg8:
                        if x==ls[0]:
                            r1=x
                    for y in reg8:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+s1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                    #sub reg,imm
                if(ls[0] in reg32 and ls[1] in ls3):
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            s1=ls3[j]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+s1.zfill(8)[::-1]
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                if(ls[0] in reg16 and ls[1] in ls3):
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            s1=ls3[j]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+s1.zfill(8)[::-1]
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
               
                if(ls[0] in reg16 and ls[1] in ls3):
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            s1=ls3[j]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+s1.zfill(8)[::-1]
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
            if(ls1[i]=="mul"): # mul instruct
                if(ls1[i+1] in reg32 or ls1[i+1] in reg16 or ls1[i+1]in reg8):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+"M"
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
            if(ls1[i]=="div"):  # div instruct
                if(ls1[i+1] in reg32 or ls1[i+1] in reg16 or ls1[i+1]in reg8):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+"D"
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
            if(ls1[i]=="jmp"):    #jmp instruct
                for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                f=p1
                fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                add=add+addr(f)
            if(ls1[i]=='inc'): # inc
                if(ls1[i+1] in reg32):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                if(ls1[i+1] in reg16):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f="6"+p1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                if(ls1[i+1] in reg8):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f="8"+p1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
            if(ls1[i]=='dec'): #dec
                if(ls1[i+1] in reg32):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                if(ls1[i+1] in reg16):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f="6"+p1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                if(ls1[i+1] in reg8):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f="8"+p1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
            if(ls1[i]=="xor"): # XOR instruct reg,reg
                ls=ls1[i+1].split(",")
                # for xor eax,ebx
                if(ls[0] in reg32 and ls[1] in reg32):
                    for x in reg32:
                        if x==ls[0]:
                            r1=x
                    for y in reg32:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+s1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                
                if(ls[0] in reg16 and ls[1] in reg16):
                    for x in reg16:
                        if x==ls[0]:
                            r1=x
                    for y in reg16:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+s1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                
                if(ls[0] in reg8 and ls[1] in reg8):
                    for x in reg8:
                        if x==ls[0]:
                            r1=x
                    for y in reg8:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+s1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)

            if(ls1[i]=="cmp"): # cmp instruct 
                ls=ls1[i+1].split(",")
                if(ls[0] in reg32 and ls[1] in reg32):
                    for x in reg32:
                        if x==ls[0]:
                            r1=x
                    for y in reg32:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+s1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
               
                if(ls[0] in reg16 and ls[1] in reg16):
                    for x in reg16:
                        if x==ls[0]:
                            r1=x
                    for y in reg16:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+s1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                
                if(ls[0] in reg8 and ls[1] in reg8):
                    for x in reg8:
                        if x==ls[0]:
                            r1=x
                    for y in reg8:
                        if y==ls[1]:
                            r2=y
                    for k in range(l4):
                        if ls4[k]==r1:
                            if ls4[k+1]==r2:
                                s1=ls4[k+2]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+s1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
              #cmp reg,imm
                if(ls[0] in (reg32 or reg16 or reg8) and ls[1].isdigit()):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+ls[1].zfill(2)
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+cal_add(f)
            if(ls1[i] in jmpint):     #jmp instruction
                for k in range(l5):
                    if str(lcnt) == ls5[k]:
                        p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                f=p1
                fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                add=add+addr(f)
            if(ls1[i]=="push"):    #push
                if(ls1[i+1] in reg32):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                if(ls1[i+1] in ls2):
                    for k in range(l2):
                        if ls2[k]==ls1[i+1]:
                            s1=ls2[k+2]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+s1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
            #call instruction
            if(ls1[i]=="call"):
                if(ls1[i+1]=="printf"):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1+str(0).zfill(8)
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
            #string instruction
            if(ls1[i] in repint):
                if(ls1[i+1]=="movsb"):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                elif(ls1[i+1]=="movsw"):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+cal_add(obj)
                elif(ls1[i+1]=="movsd"):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                elif(ls1[i+1]=="stosb"):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                elif(ls1[i+1]=="stosw"):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                elif(ls1[i+1]=="stosd"):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                elif(ls1[i+1]=="cmpsb"):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                elif(ls1[i+1]=="cmpsw"):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                elif(ls1[i+1]=="cmpsd"):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                
                elif(ls1[i+1]=="lodsb"):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+addr(f)
                elif(ls1[i+1]=="lodsw"):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                    add=add+add(f)
                else:
                    if(ls1[i+1]=="lodsd"):
                        for k in range(l5):
                            if str(lcnt) == ls5[k]:
                                p=ls5[k+2]
                        for l in range(l6):
                            if str(p)==ls6[l]:
                                p1=ls6[l+1]
                        f=p1
                        fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                        add=add+addr(f)
                if(ls1[i]=="std"):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            p1=ls6[l+1]
                    f=p1
                    fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                add=add+addr(f)
            #cld instruction
            if(ls1[i]=="cld"):
                for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                f=p1
                fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                add=add+addr(f)
            #ret instruction
            if(ls1[i]=="ret"):
                for k in range(l5):
                    if str(lcnt) == ls5[k]:
                        p=ls5[k+2]
                for l in range(l6):
                    if str(p)==ls6[l]:
                        p1=ls6[l+1]
                f=p1
                fout.write("\t\t\t"+str(add).zfill(8)+"\t"+str(add_space(f))+"\n")
                add=add+addr(f)

            


                    
                    
object_code("add2.asm","symbol.txt","literal.txt","mod.txt","inter_code.txt","opc.txt")


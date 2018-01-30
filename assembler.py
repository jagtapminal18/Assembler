from sys import *
def symtable(fnm):
    cc=['je','jle','jge','jl','jg','jz']
    sym=[]
    size=[]
    d_u=[]
    count=[]
    stype=[]
    lcntl=[]
    lable=[]
    error=[]
    dfi=0
    dfc=0
    ufi=0
    ufc=0
    dfq=0
    ufq=0
    lcnt=0
    lablecnt=0
    raddr=[]
    rinitaddr=0
    uinitaddr=0
    i=0
    fout=open("symbol.txt","w")
    fobj=open(fnm,"r")
    l=fobj.readline()
    c=len(l)
    #print("line_no","sym_name "," size ","  d/u "," count ","addr")
    for l in fobj:
        lcnt+=1
        ch=l.split()
        #print(ch)
        chl=len(ch)
        for i in range(chl):
            if(ch[i].isalnum):
                if(ch[i]=='dd'):
                    if(ch[i+1].isalpha()==True):
                        error.append("mismatch data")
                    else:
                        s=ch[i+1].split(',')
                        sz=len(s)*4
                        raddr.append(rinitaddr)
                        lcntl.append((lcnt))
                        sym.append(ch[i-1])
                        size.append(sz)
                        d_u.append("d")
                        stype.append("int")
                        count.append(dfi)
                        dfi+=1
                        rinitaddr+=sz
                elif(ch[i]=='db'):
                    s=ch[i+1].split(',')
                    #print(s)
                    m=s[0].split('"')
                    #print(m)
                    sz=len(m[0])*1
                    raddr.append(rinitaddr)
                    lcntl.append(lcnt)
                    sym.append(ch[i-1])
                    size.append(sz)
                    d_u.append("d")
                    stype.append("char")
                    count.append(dfc)
                    rinitaddr+=sz
                    dfc+=1
                elif(ch[i]=='dq'):
                    sz=4
                    raddr.append(rinitaddr)
                    lcnt1.append(lcnt)
                    sym.append(ch[i-1])
                    size.append(4)
                    d_u.append("d")
                    stype.append("qword")
                    count.append(dfq)
                    dfq+=1
                    rinitaddr+=sz
                elif(ch[i]=="resd"):
                    sz=4
                    rinitaddr=0
                    raddr.append(rinitaddr)
                    lcntl.append(lcnt)
                    sym.append(ch[i-1])
                    size.append(4)
                    d_u.append("d")
                    count.append(ufi)
                    ufi+=1
                elif(ch[i]=='resq'):
                    raddr.append(rinitaddr)
                    sym.append(ch[i-1])
                    size.append(4)
                    d_u.append("d")
                    count.append(ufq)
                    dfc+=1
                    rinitaddr+=sz
                elif(ch[i]=="resb"):
                    raddr.append(uinitaddr)
                    lcntl.append(lcnt)
                    sym.append(ch[i-1])
                    size.append(1)
                    d_u.append("d")
                    count.append(ufc)
                    ufc+=1
                    rinitaddr+=sz
                if(ch[i-1].endswith(":")):
                    s=ch[i-1].split(":")
                    raddr.append(str(00000000))
                    lcntl.append(lcnt)
                    sym.append(s[0])
                    size.append(0)
                    d_u.append("u")
                    count.append(lablecnt)
                    lable.append(ch[i-1])
                    lablecnt+=1
            if(ch[i-1]=="jmp"):
                if ch[i] not in lable:
                    error.append("unconditional- undefine lable")
            if ch[i-1] in cc:
                if ch[i] not in lable:
                    error.append("lable not found")
                    
                            
                        


                        
    lensym=len(sym)
    j=0
    cnt=0
    newls=[]
    while(j<lensym):
        for j in range(lensym):
            if(sym[j-1]!=sym[j]):
                print(j+1,end="     ")
                print(lcntl[j],end="      ")
                print(sym[j],end="        ")
                print(size[j],end="       ")
                print(d_u[j],end="        ")
                print(count[j],end="      ")
                print(raddr[j],end="    ")
                print()
                newls.append(sym[j])
                j+=1
            else:
                print(sym[j],"\t")
                print(size[j],"\t")
                print("redf","\t")
                print(count[j],"\t")
               # print(raddr[j],"\t")
                print()
                j+=1
   # fout.write("sym no"+"\t"+"lineno"+"\t"+"symbol"+"\t"+"size"+"\t"+"Address"+"\n")
    for j in range(0,len(newls)):
        fout.write(str(j+1)+"\t"+str(lcntl[j])+"\t"+str(newls[j])+"\t"+str(size[j])+"\t"+str(raddr[j]).zfill(8)+"\n")
    fobj1=open("serror.txt","w")
    fobj1.write("errno"+"\t"+"error"+"\n")
    for j in  range(0,len(error)):
        fobj1.write(str(lcntl[j])+"\t"+error[j]+"\n")

#symtable("add2.asm")

def inter_code(fnm1,fnm2):
    reg32=['eax','ebx','ecx','edx','esi','edi','esp','ebp']
    reg16=['ax','bx','cx','dx']
    reg8=['ah','bh','ch','dh','al','bl','cl','dl']
    logint=['and','or','xor']
    jmpint=['jmp','jne','je','jz','jg','jge','jl','jle']
    strint32=['movsd','stosd','scasd']
    strint16=['movsw','stosw','scasw']
    strint8=['movsb','stosb','scasb']
    lcnt=[]
    addr=[]
    line=[]
    tline=[]
    litcnt=0
    litcnt1=[]
    lit=[]
    opindex=[]
    op=[]
    opc=[]
    maccnt=0
    macnm=[]
    macprm=[]
    mc=[]
    initaddr=00000000
    lc=0
    #fout=open("opcode_file.txt","w")
    f1=open(fnm1,'r')
    l1=f1.readline()
    f2=open(fnm2,"r")
    l2=f2.readline()
    print("line_no"," address","\tline","\ttransform line")
    for l2 in f2:
        sp2=l2.split()
        #print(sp2)
        spl2=len(sp2)
    for l1 in f1:
         lc+=1
         sp1=l1.split()
         #print(sp1)
         spl1=len(sp1)
         for i in range(spl1):
             if(sp1[i]=="mov"):                # mov instruction
                 s=sp1[i+1].split(",")   
                 if s[0] in reg32:
                     indx=reg32.index(s[0])+1
                     tl1=l1.replace(s[0],"reg#"+str(indx)+"3")
                     if s[1] in reg32:
                         indx=reg32.index(s[1])+1
                         tl2=tl1.replace(s[1],"reg#"+str(indx)+"3")
                         tl3=tl2.replace(sp1[0],"op#"+str(1))
                         initaddr+=2
                         addr.append(initaddr)
                         line.append(l1)
                         lcnt.append(lc)
                         tline.append(tl3)
                         opindex.append(str(1))
                         opc.append("1A")
                         op.append("mov r32,r32")
                         #fout.write("mov r32,r32"+"\t"+"op#1\n")
                     elif(s[1].startswith("dword")):
                         k=s[1].split('[')
                         m=k[1].split(']')
                         if(m[0].isalpha()):
                             tl2=tl1.replace(s[1],"sym#"+m[0])
                             tl3=tl2.replace(sp1[0],"op#"+str(2))
                             initaddr+=6
                             addr.append(initaddr)
                             line.append(l1)
                             lcnt.append(lc)
                             tline.append(tl3)
                             opindex.append(str(2))
                             op.append("mov r32,m")
                             opc.append("2B")
                     elif(s[1].isdigit()):
                         litcnt+=1
                         lit.append(s[1])
                         tl2=tl1.replace(s[1],"lit#"+s[1])
                         tl3=tl2.replace(sp1[0],"op#"+str(3))
                         initaddr+=2
                         addr.append(initaddr)
                         line.append(l1)
                         lcnt.append(lc)
                         tline.append(tl3)
                         opindex.append(str(3))
                         op.append("mov r32,i")
                         opc.append("3c")
                         litcnt1.append(litcnt)
                 if(s[0].startswith("dword")):
                     k=s[0].split('[')
                     m=k[1].split(']')
                     if(m[0].isalpha()):
                         tl1=l1.replace(s[0],"sym#"+m[0])
                         if s[1] in reg32:
                             indx=reg32.index(s[1])+1
                             tl2=tl1.replace(s[1],"reg#"+str(indx)+"3")
                             tl3=tl2.replace(sp1[0],"op#"+str(4))
                             initaddr+=6
                             addr.append(initaddr)
                             line.append(l1)
                             lcnt.append(lc)
                             tline.append(tl3)
                             opindex.append(str(4))
                             op.append("mov m,r32")
                             opc.append("4D")
                 if s[0] in reg16:
                     indx=reg16.index(s[0])+1
                     tl1=l1.replace(s[0],"reg#"+str(indx)+"6")
                     if s[1] in reg16:
                         indx=reg16.index(s[1])+1
                         tl2=tl1.replace(s[1],"reg#"+str(indx)+"6")
                         tl3=tl2.replace(sp1[0],"op#"+str(5))
                         initaddr+=2
                         addr.append(initaddr)
                         line.append(l1)
                         lcnt.append(lc)
                         tline.append(tl3)
                         opindex.append(str(5))
                         op.append("mov r16,r16")
                         opc.append("5E")
                     elif(s[1].isalpha()):
                         if(s[1]==sp2[1]):
                             tl2=tl1.replace(s[1],"sym#"+s[1])
                             tl3=tl2.replace(sp1[0],"op#"+str(6))
                             initaddr+=6
                             addr.append(initaddr)
                             line.append(l1)
                             lcnt.append(lc)
                             tline.append(tl3)
                             opindex.append(str(6))
                             op.append("mov r16,m")
                             opc.append("6F")
                     elif(s[1].isdigit()):
                         litcnt+=1
                         lit.append(s[1])
                         tl2=tl1.replace(s[1],"sym#"+s[1])
                         tl3=tl2.replace(sp1[0],"op#"+str(7))
                         initaddr+=2
                         addr.append(initaddr)
                         line.append(l1)
                         lcnt.append(lc)
                         tline.append(tl3)
                         opindex.append(str(7))
                         op.append("mov r16,i")
                         opc.append("7G")
                         litcnt1.append(litcnt)
                 if(s[0].isalpha()):
                     if(s[0]==sp1[1]):
                         tl1=l1.replace(s[0],"sym#"+s[0])
                         if s[1] in reg16:
                             indx=reg16.index(s[1])+1
                             tl2=tl1.replace(s[1],"reg#"+str(indx)+"6")
                             tl3=tl2.replace(sp1[0],"op#"+str(8))
                             initaddr+=6
                             addr.append(initaddr)
                             line.append(l1)
                             lcnt.append(lc)
                             tline.append(tl3)
                             opindex.append(str(8))
                             op.append("mov m,r16")
                             opc.append("8H")
                 if s[0] in reg8:
                     indx=reg8.index(s[0])+1
                     tl1=l1.replace(s[0],"reg#"+str(indx)+"8")
                     if s[1] in reg8:
                         indx=reg8.index(s[1])+1
                         tl2=tl1.replace(s[1],"reg#"+str(indx)+"8")
                         tl3=tl2.replace(sp1[0],"op#"+str(9))
                         initaddr+=2
                         addr.append(initaddr)
                         line.append(l1)
                         lcnt.append(lc)
                         tline.append(tl3)
                         opindex.append(str(9))
                         op.append("mov r8,r8")
                         opc.append("9I")
                     elif(s[1].startswith("byte")):
                         k=s[1].split('[')
                         m=k[1].split(']')
                         if(m[0].isalpha()):
                             tl2=tl1.replace(s[1],"sym#"+m[0])
                             tl3=tl2.replace(sp1[0],"op#"+str(10))
                             initaddr+=6
                             addr.append(initaddr)
                             line.append(l1)
                             lcnt.append(lc)
                             tline.append(tl3)
                             opindex.append(str(10))
                             op.append("mov r8,m")
                             opc.append("10J")
                     elif(s[1].isdigit()):
                         litcnt+=1
                         lit.append(s[1])
                         tl2=tl1.replace(s[1],"lit#"+s[1])
                         tl3=tl2.replace(sp1[0],"op#"+str(11))
                         initaddr+=2
                         addr.append(initaddr)
                         addr.append(initaddr)
                         line.append(l1)
                         lcnt.append(lc)
                         tline.append(tl3)
                         opindex.append(str(11))
                         op.append("mov r8,i")
                         opc.append("11K")
                         litcnt1.append(litcnt)
                 if(s[0].startswith("byte")):
                     k=s[0].split('[')
                     m=k[1].split(']')
                     if(m[0].isalpha()):
                         tl1=l1.replace(s[0],"sym#"+m[0])
                         if s[1] in reg8:
                             indx=reg8.index(s[1])+1
                             tl2=tl1.replace(s[1],"reg#"+str(indx)+"8")
                             tl3=tl2.replace(sp1[0],"op#"+str(12))
                             initaddr+=6
                             addr.append(initaddr)
                             line.append(l1)
                             lcnt.append(lc)
                             tline.append(tl3)
                             opindex.append(str(12))
                             op.append("mov m,r8")        
                             opc.append("12L")
             if(sp1[i]=="add"):                 # add instruction
                 s=sp1[i+1].split(",")
                 if s[0] in reg32:
                     indx=reg32.index(s[0])+1
                     tl1=l1.replace(s[0],"reg#"+str(indx)+"3")
                     if s[1] in reg32:
                         indx=reg32.index(s[1])+1
                         tl2=tl1.replace(s[1],"reg#"+str(indx)+"3")
                         tl3=tl2.replace(sp1[0],"op#"+str(13))
                         initaddr+=2
                         addr.append(initaddr)
                         line.append(l1)
                         lcnt.append(lc)
                         tline.append(tl3)
                         opindex.append(str(13))
                         op.append("add r,r")
                         opc.append("13M")
                     elif(s[1].startswith("dword")):
                         k=s[1].split('[')
                         m=k[1].split(']')
                         if(m[0].isalpha()):
                             tl1=l1.replace(s[1],"lit#"+m[0])
                             tl2=tl1.replace(sp1[0],"op#"+str(14))
                             initaddr+=6
                             addr.append(initaddr)
                             line.append(l1)
                             lcnt.append(lc)
                             opindex.append(str(14))
                             op.append("add r,m")
                             opc.append("14N")
                 if(s[0].startswith("dword")):
                     k=s[0].split('[')
                     m=k[1].split(']')
                     if(m[0].isalpha()):
                         tl1=l1.replace(s[0],"sym#"+m[0])
                         if s[1] in reg32:
                             indx=reg32.index(s[1])+1
                             tl2=tl1.replace(s[1],"reg#"+str(indx)+"3")
                             tl3=tl2.replace(sp1[0],"op#"+str(15))
                             initaddr+=6
                             addr.append(initaddr)
                             line.append(l1)
                             lcnt.append(lc)
                             tline.append(tl3)
                             opindex.append(str(15))
                             op.append("add m,r")
                             opc.append("15O")
                 if s[0] in reg32:
                     indx=reg32.index(s[0])+1
                     tl1=l1.replace(s[0],"reg#"+str(indx)+"3")
                     tl2=tl1.replace(s[1],"lit#"+s[1])
                     if(s[1].isdigit()):
                         litcnt+=1
                         lit.append(s[1])
                         tl3=tl2.replace(sp1[0],"op#"+str(16))
                         initaddr+=2
                         addr.append(initaddr)
                         line.append(l1)
                         lcnt.append(lc)
                         tline.append(tl3)
                         opindex.append(str(16))
                         op.append("add r,i")
                         opc.append("16P")
                         litcnt1.append(litcnt)
                 if s[0] in reg16:
                     indx=reg16.index(s[0])+1
                     tl1=l1.replace(s[0],"reg#"+str(indx)+"6")
                     if s[1] in reg16:
                         indx=reg16.index(s[1])+1
                         tl2=tl1.replace(s[1],"reg#"+str(indx)+"6")
                         tl3=tl2.replace(sp1[0],"op#"+str(17))
                         initaddr+=2
                         addr.append(initaddr)
                         line.append(l1)
                         lcnt.append(lc)
                         tline.append(tl3)
                         opindex.append(str(17))
                         op.append("add r16,r16")
                         opc.append("17Q")
                     elif(s[1].isalpha()):
                         if(s[1]==sp2[1]):
                             tl2=tl1.replace(s[1],"sym#"+s[1])
                             tl3=tl2.replace(sp1[0],"op#"+str(18))
                             initaddr+=6
                             addr.append(initaddr)
                             line.append(l1)
                             lcnt.append(lc)
                             tline.append(tl3)
                             opindex.append(str(18))
                             op.append("add r16,m")
                             opc.append("18R")
                     elif(s[1].isdigit()):
                         tl2=tl1.replace(s[1],"lit#"+s[1])
                         tl3=tl2.replace(sp1[0],"op#"+str(19))
                         initaddr+=2
                         addr.append(initaddr)
                         line.append(l1)
                         lcnt.append(lc)
                         tline.append(tl3)
                         opindex.append(str(19))
                         op.append("add r16,i")
                         opc.append("19S")
                 if(s[0].isalpha()):
                     if(s[0]==sp1[1]):
                         tl1=l1.replace(s[0],"sym#"+s[0])
                         if s[1] in reg16:
                             indx=reg16.index(s[1])+1
                             tl2=tl1.replace(s[1],"reg#"+str(indx)+"6")
                             tl3=tl2.replace(sp1[0],"op#"+str(20))
                             initaddr+=6
                             addr.append(initaddr)
                             line.append(l1)
                             lcnt.append(lc)
                             tline.append(tl3)
                             opindex.append(str(20))
                             op.append("add m,r16")
                             opc.append("20T")
                 if s[0] in reg8:
                     indx=reg8.index(s[0])+1
                     tl1=l1.replace(s[0],"reg#"+str(indx)+"8")
                     if s[1] in reg8:
                         indx=reg8.index(s[1])+1
                         tl2=tl1.replace(s[1],"reg#"+str(indx)+"8")
                         tl3=tl2.replace(sp1[0],"op#"+str(21))
                         initaddr+=2
                         addr.append(initaddr)
                         line.append(l1)
                         lcnt.append(lc)
                         tline.append(tl3)
                         opindex.append(str(21))
                         op.append("add r8,r8")
                         opc.append("21U")
                     elif(s[1].startswith("byte")):
                         k=s[1].split('[')
                         m=k[1].split(']')
                         if(m[0].isalpha()):
                             tl2=tl1.replace(s[1],"sym#"+m[0])
                             tl3=tl2.replace(sp1[0],"op#"+str(22))
                             initaddr+=6
                             addr.append(initaddr)
                             line.append(l1)
                             lcnt.append(lc)
                             tline.append(tl3)
                             opindex.append(str(22))
                             op.append("add r8,m")
                             opc.append("22V")
                 if(s[0].startswith("byte")):
                     if(m[0].isalpha()):
                         tline.append(m[0])
                         if s[1] in reg8:
                             indx=reg32.index(s[1])+1
                             tl1=l1.replace(s[1],"reg#"+str(indx)+"8")
                             tl2=tl1.replace(sp1[0],"op#"+str(23))
                             initaddr+=6
                             addr.append(initaddr)
                             line.append(l1)
                             lcnt.append(lc)
                             tline.append(tl2)
                             opindex.append(str(23))
                             op.append("add m,r8")
                             opc.append("23W")
                 if s[0] in reg8:
                     indx=reg8.index(s[0])+1
                     tl1=l1.replace(s[0],"reg#"+str(indx)+"8")
                     if(s[1].isdigit()==True):
                         tl2=tl1.replace(sp1[0],"op#"+str(24))
                         initaddr+=2
                         addr.append(initaddr)
                         line.append(l1)
                         lcnt.append(lc)
                         tline.append(tl2)
                         opindex.append(str(24))
                         op.append("add r8,i")
                         opc.append("24X")
             if(sp1[i]=="sub"):                   #sub instruction
                 s=sp1[i+1].split(",")   
                 if s[0] in reg32:
                    indx=reg32.index(s[0])+1
                    tl1=l1.replace(s[0],"reg#"+str(indx)+"3")
                    if s[1] in reg32:
                        indx=reg32.index(s[1])+1
                        tl2=tl1.replace(s[1],"reg#"+str(indx)+"3")
                        tl3=tl2.replace(sp1[0],"op#"+str(25))
                        initaddr+=2
                        addr.append(initaddr)
                        line.append(l1)
                        lcnt.append(lc)
                        tline.append(tl3)
                        opindex.append(str(25))
                        op.append("sub r32,r32")
                        opc.append("25Y")
                    elif(s[1].startswith("dword")):
                        k=s[1].split('[')
                        m=k[1].split(']')
                        if(m[0].isalpha()):
                            tl2=tl1.replace(s[1],"sym#"+m[0])
                            tl3=tl2.replace(sp1[0],"op#"+str(26))
                            initaddr+=6
                            addr.append(initaddr)
                            line.append(l1)
                            lcnt.append(lc)
                            tline.append(tl3)
                            opindex.append(str(26))
                            op.append("sub r32,m")
                            opc.append("26Z")
                 if(s[0].startswith("dword")):
                     k=s[0].split('[')
                     m=k[1].split(']')
                     if(m[0].isalpha()):
                         tl1=l1.replace(s[0],"sym#"+m[0])
                         if s[1] in reg32:
                             indx=reg32.index(s[1])+1
                             tl1=l1.replace(s[1],"reg#"+str(indx)+"3")
                             tl2=tl1.replace(sp1[0],"op#"+str(27))
                             initaddr+=6
                             addr.append(initaddr)
                             line.append(l1)
                             lcnt.append(lc)
                             tline.append(tl2)
                             opindex.append(str(27))
                             op.append("sub m,r32")
                             opc.append("27A")
                 if s[0] in reg32:
                     indx=reg32.index(s[0])+1
                     tl1=l1.replace(s[0],"reg#"+str(indx)+"3")
                     if(s[1].isdigit()==True):
                         litcnt+=1
                         lit.append(s[1])
                         tl2=tl1.replace(sp1[0],"op#"+str(28))
                         initaddr+=2
                         addr.append(initaddr)
                         line.append(l1)
                         lcnt.append(lc)
                         tline.append(tl2)
                         opindex.append(str(28))
                         op.append("sub r32,i")
                         opc.append("28B")
                         litcnt1.append(litcnt)
                 if s[0] in reg16:
                     indx=reg16.index(s[0])+1
                     tl1=l1.replace(s[0],"reg#"+str(indx)+"6")
                     if s[1] in reg16:
                         indx=reg16.index(s[1])+1
                         tl2=tl1.replace(s[1],"reg#"+str(indx)+"6")
                         tl3=tl2.replace(sp1[0],"op#"+str(29))
                         initaddr+=2
                         addr.append(initaddr)
                         line.append(l1)
                         lcnt.append(lc)
                         tline.append(tl3)
                         opindex.append(str(29))
                         op.append("sub r16,r16")
                         opc.append("29C")
                     elif(s[1].isalpha()):
                         if(s[1]==sp2[1]):
                             tl2=tl1.replace(s[1],"sym#"+s[1])
                             tl3=tl2.replace(sp1[0],"op#"+str(30))
                             initaddr+=6
                             addr.append(initaddr)
                             line.append(l1)
                             lcnt.append(lc)
                             tline.append(tl3)
                             opindex.append(str(30))
                             op.append("sub r16,m")
                             opc.append("30D")
                         elif(s[1].isdigit()):
                             litcnt+=1
                             lit.append(s[1])
                             tl2=tl1.replace(s[1],"sym#"+s[1])
                             tl3=tl2.replace(sp1[0],"op#"+str(31))
                             initaddr+=2
                             addr.append(initaddr)
                             line.append(l1)
                             lcnt.append(lc)
                             tline.append(tl3)
                             opindex.append(str(31))
                             op.append("sub r16,i")
                             opc.append("31E")
                             litcnt1.append(litcnt)
                 if(s[0].isalpha()):
                     if(s[0]==sp1[1]):
                         tl1=l1.replace(s[0],"sym#"+s[0])
                         if s[1] in reg16:
                             indx=reg16.index(s[1])+1
                             tl2=tl1.replace(s[1],"reg#"+str(indx)+"6")
                             tl3=tl2.replace(sp1[0],"op#"+str(32))
                             initaddr+=6
                             addr.append(initaddr)
                             line.append(l1)
                             lcnt.append(lc)
                             tline.append(tl3)
                             opindex.append(str(32))
                             op.append("sub m,r16")
                             opc.append("32F")
                 if s[0] in reg8:
                     indx=reg8.index(s[0])+1
                     tl1=l1.replace(s[0],"reg#"+str(indx)+"8")
                     if s[1] in reg8:
                         indx=reg8.index(s[1])+1
                         tl2=tl1.replace(s[1],"reg#"+str(indx)+"8")
                         tl3=tl2.replace(sp1[0],"op#"+str(33))
                         initaddr+=2
                         addr.append(initaddr)
                         line.append(l1)
                         lcnt.append(lc)
                         tline.append(tl3)
                         opindex.append(str(33))
                         op.append("sub r8,r8")
                         opc.append("33G")
                     elif(s[1].startswith("byte")):
                         m=s[1].split('[')
                         if(m[1].isalpha()):
                             tl2=tl1.replace(s[1],"sym#"+m[1])
                             tl3=tl2.replace(sp1[0],"op#"+str(34))
                             initaddr+=6
                             addr.append(initaddr)
                             line.append(l1)
                             lcnt.append(lc)
                             tline.append(tl3)
                             opindex.append(str(34))
                             op.append("sub r8,m")
                             opc.append("34H")
                 if(s[0].startswith("byte")):
                     if(m[0].isalpha()):
                         tline.append(m[0])
                         if s[1] in reg8:
                             indx=reg32.index(s[1])+1
                             tl1=l1.replace(s[1],"reg#"+str(indx)+"8")
                             tl2=tl1.replace(sp1[0],"op#"+str(35))
                             initaddr+=6
                             addr.append(initaddr)
                             line.append(l1)
                             lcnt.append(lc)
                             tline.append(tl2)
                             opindex.append(str(35))
                             op.append("sub m,r8")
                             opc.append("35I")
                 if s[0] in reg8:
                     indx=reg8.index(s[0])+1
                     tl1=l1.replace(s[0],"reg#"+str(indx)+"8")
                     if(s[1].isdigit()==True):
                         tl2=tl1.replace(sp1[0],"op#"+str(36))
                         initaddr+=2
                         addr.append(initaddr)
                         line.append(l1)
                         lcnt.append(lc)
                         tline.append(tl2)
                         opindex.append(str(36))
                         op.append("sub r8,i")
                         opc.append("36J")
             if sp1[i] in logint:           #logical instruction and 
                
                 s=sp1[i+1].split(",")       # or xor
                 if s[0] in reg32:
                     indx=reg32.index(s[0])+1
                     tl1=l1.replace(s[0],"reg#"+str(indx)+"3")
                     if s[1] in reg32:
                         indx=reg32.index(s[1])+1
                         tl2=tl1.replace(s[1],"reg#"+str(indx)+"3")
                         tl3=tl2.replace(sp1[0],"op#"+str(i)+str(37))
                         initaddr+=2
                         addr.append(initaddr)
                         line.append(l1)
                         lcnt.append(lc)
                         tline.append(tl3)
                         opindex.append(str(i)+str(37))
                         op.append(sp1[i]+" r32,r32")
                         opc.append(str(i)+"37K")
                     elif(s[1].startswith("dword")):
                         k=s[1].split('[')
                         m=k[1].split(']')
                         if(m[0].isalpha()):
                             tl2=tl1.replace(s[1],"sym#"+m[0])
                             tl3=tl2.replace(sp1[0],"op#"+str(i)+str(38))
                             initaddr+=6
                             addr.append(initaddr)
                             line.append(l1)
                             lcnt.append(lc)
                             tline.append(tl3)
                             opindex.append(str(i)+str(38))
                             op.append(sp1[i]+" r32,m")
                             opc.append(str(i)+"38L")
                     elif(s[1].isdigit()):
                         litcnt+=1
                         lit.append(s[1])
                         tl2=tl1.replace(s[1],"lit#"+s[1])
                         tl3=tl2.replace(sp1[0],"op#"+str(i)+str(39))
                         initaddr+=2
                         addr.append(initaddr)
                         addr.append(initaddr)
                         line.append(l1)
                         lcnt.append(lc)
                         tline.append(tl3)
                         opindex.append(str(i)+str(39))
                         op.append(sp1[i]+" r32,i")
                         opc.append(str(i)+"39M")
                         litcnt1.append(litcnt)
                 if(s[0].startswith("dword")):
                     k=s[0].split('[')
                     m=k[1].split(']')
                     if(m[0].isalpha()):
                         tl1=l1.replace(s[0],"sym#"+m[0])
                         if s[1] in reg32:
                             indx=reg32.index(s[1])+1
                             tl2=tl1.replace(s[1],"reg#"+str(indx)+"3")
                             tl3=tl2.replace(sp1[0],"op#"+str(i)+str(40))
                             initaddr+=6
                             addr.append(initaddr)
                             line.append(l1)
                             lcnt.append(lc)
                             tline.append(tl3)
                             opindex.append(str(i)+str(40))
                             op.append(sp1[i]+" m,r32")
                             opc.append(str(i)+"40N")
                 if s[0] in reg16:
                     indx=reg16.index(s[0])+1
                     tl1=l1.replace(s[0],"reg#"+str(indx)+"6")
                     if s[1] in reg16:
                         indx=reg16.index(s[1])+1
                         tl2=tl1.replace(s[1],"reg#"+str(indx)+"6")
                         tl3=tl2.replace(sp1[0],"op#"+str(i)+str(41))
                         initaddr+=2
                         addr.append(initaddr)
                         line.append(l1)
                         lcnt.append(lc)
                         tline.append(tl3)
                         opindex.append(str(i)+str(41))
                         op.append(sp1[i]+" r16,r16")
                         opc.append(str(i)+"41O")
                     elif(s[1].isalpha()):
                         if(s[1]==sp2[1]):
                             tl2=tl1.replace(s[1],"sym#"+s[1])
                             tl3=tl2.replace(sp1[0],"op#"+str(i)+str(42))
                             initaddr+=6
                             addr.append(initaddr)
                             line.append(l1)
                             lcnt.append(lc)
                             tline.append(tl3)
                             opindex.append(str(i)+str(42))
                             op.append(sp1[i]+" r16,m")
                             opc.append(str(i)+"42P")
                     elif(s[1].isdigit()):
                         tl2=tl1.replace(s[1],"sym#"+s[1])
                         tl3=tl2.replace(sp1[0],"op#"+str(i)+str(43))
                         initaddr+=2
                         addr.append(initaddr)
                         line.append(l1)
                         lcnt.append(lc)
                         tline.append(tl3)
                         opindex.append(str(i)+str(43))
                         op.append(sp1[i]+" r16,i")
                         opc.append(str(i)+"43Q")
                 if(s[0].isalpha()):
                     if(s[0]==sp1[1]):
                         tl1=l1.replace(s[0],"sym#"+s[0])
                         if s[1] in reg16:
                             indx=reg16.index(s[1])+1
                             tl2=tl1.replace(s[1],"reg#"+str(indx)+"6")
                             tl3=tl2.replace(sp1[0],"op#"+str(i)+str(44))
                             initaddr+=6
                             addr.append(initaddr)
                             line.append(l1)
                             lcnt.append(lc)
                             tline.append(tl3)
                             opindex.append(str(i)+str(44))
                             op.append(sp1[i]+" m,r16")
                             opc.append(str(i)+"44R")
                 if s[0] in reg8:
                     indx=reg8.index(s[0])+1
                     tl1=l1.replace(s[0],"reg#"+str(indx)+"8")
                     if s[1] in reg8:
                         indx=reg8.index(s[1])+1
                         tl2=tl1.replace(s[1],"reg#"+str(indx)+"8")
                         tl3=tl2.replace(sp1[0],"op#"+str(i)+str(45))
                         initaddr+=2
                         addr.append(initaddr)
                         line.append(l1)
                         lcnt.append(lc)
                         tline.append(tl3)
                         opindex.append(str(i)+str(45))
                         op.append( sp1[i]+" r8,r8")
                         opc.append(str(i)+"45S")
                     elif(s[1].startswith("byte")):
                         tl2=tl1.replace(s[1],"lit#"+s[1])
                         tl3=tl2.replace(sp1[0],"op#"+str(i)+str(46))
                         initaddr+=6
                         addr.append(initaddr)
                         line.append(l1)
                         lcnt.append(lc)
                         tline.append(tl3)
                         opindex.append(str(i)+str(46))
                         op.append(sp1[i]+" r8,m")
                         opc.append(str(i)+"46T")
                 if(s[0].startswith("byte")):
                     if(m[0].isalpha()):
                         tline.append(m[0])
                         if s[1] in reg8:
                             indx=reg8.index(s[1])+1
                             tl1=l1.replace(s[1],"reg#"+str(indx)+"8")
                             tl2=tl1.replace(sp1[0],"op#"+str(i)+str(47))
                             initaddr+=6
                             addr.append(initaddr)
                             line.append(l1)
                             lcnt.append(lc)
                             tline.append(tl2)
                             opindex.append(str(i)+str(47))
                             op.append(sp1[i]+" m,r8")
                             opc.append(str(i)+"47U")
                 if s[0] in reg8:
                     indx=reg8.index(s[0])+1
                     tl1=l1.replace(s[0],"reg#"+str(indx)+"8")
                     if(s[1].isdigit()==True):
                         tl2=tl1.replace(sp1[0],"op#"+str(i)+str(48))
                         initaddr+=2
                         addr.append(initaddr)
                         line.append(l1)
                         lcnt.append(lc)
                         tline.append(tl2)
                         opindex.append(str(i)+str(48))
                         op.append(sp1[i]+" r8,i")
                         opc.append(str(i)+"48V")
             if(sp1[i]=="inc"):                 # inc instruction
                 if sp1[i+1] in reg32:
                     indx=reg32.index(sp1[i+1])+1
                     tl1=l1.replace(sp1[i+1],"reg#"+str(indx)+"3")
                     tl2=tl1.replace(sp1[0],"op#"+str(49))
                     initaddr+=2
                     addr.append(initaddr)
                     line.append(l1)
                     lcnt.append(lc)
                     tline.append(tl2)
                     opindex.append(str(49))
                     op.append("inc r32")
                     opc.append("49W")
                 if sp1[i+1] in reg16:
                     indx=reg16.index(sp1[i+1])+1
                     tl1=l1.replace(sp1[i+1],"reg#"+str(indx)+"6")
                     tl2=tl1.replace(sp1[0],"op#"+str(50))
                     initaddr+=2
                     addr.append(initaddr)
                     line.append(l1)
                     lcnt.append(lc)
                     tline.append(tl2)
                     opindex.append(str(50))
                     op.append("inc r16")
                     opc.append("50X")
                 if sp1[i+1] in reg8:
                     indx=reg8.index(sp1[i+1])+1
                     tl1=l1.replace(sp1[i+1],"reg#"+str(indx)+"8")
                     tl2=tl1.replace(sp1[0],"op#"+str(51))
                     initaddr+=2
                     addr.append(initaddr)
                     line.append(l1)
                     lcnt.append(lc)
                     tline.append(tl2)
                     opindex.append(str(51))
                     op.append("inc r8")
                     opc.append("51Y")
             if(sp1[i]=="dec"):                  #dec instruction
                 if sp1[i+1] in reg32:
                     indx=reg32.index(sp1[i+1])+1
                     tl1=l1.replace(sp1[i+1],"reg#"+str(indx)+"3")
                     tl2=tl1.replace(sp1[0],"op#"+str(52))
                     initaddr+=2
                     addr.append(initaddr)
                     line.append(l1)
                     lcnt.append(lc)
                     tline.append(tl2)
                     opindex.append(str(52))
                     op.append("dec r32")
                     opc.append("52Z")
                 if sp1[i+1] in reg16:
                     indx=reg16.index(sp1[i+1])+1
                     tl1=l1.replace(sp1[i+1],"reg#"+str(indx)+"6")
                     tl2=tl1.replace(sp1[0],"op#"+str(53))
                     initaddr+=2
                     addr.append(initaddr)
                     line.append(l1)
                     lcnt.append(lc)
                     tline.append(tl2)
                     opindex.append(str(53))
                     op.append("dec r16")
                     opc.append("53A")
                 if sp1[i+1] in reg8:
                     indx=reg8.index(sp1[i+1])+1
                     tl1=l1.replace(sp1[i+1],"reg#"+str(indx)+"8")
                     tl2=tl1.replace(sp1[0],"op#"+str(54))
                     initaddr+=2
                     addr.append(initaddr)
                     line.append(l1)
                     lcnt.append(lc)
                     tline.append(tl2)
                     opindex.append(str(54))
                     opc.append("54B")
                     op.append("dec r8")            
             if(sp1[i]=="push"): # push instruction 
                 if sp1[i+1] in reg32:
                     indx=reg32.index(sp1[i+1])+1
                     tl1=l1.replace(sp1[i+1],"reg#"+str(indx)+"3")
                     tl2=tl1.replace(sp1[0],"op#"+str(55))
                     initaddr+=2
                     addr.append(initaddr)
                     line.append(l1)
                     lcnt.append(lc)
                     tline.append(tl2)
                     opindex.append(str(55))
                     op.append("push r32")
                     opc.append("55C")
                 if(sp1[i+1].startswith("dword")):
                     k=sp1[1].split('[')
                     m=k[1].split(']')
                     if(m[0].isalpha()):
                         tl1=l1.replace(sp1[1],"sym#"+m[0])
                         tl2=tl1.replace(sp1[0],"op#"+str(56))
                         initaddr+=6
                         addr.append(initaddr)
                         line.append(l1)
                         lcnt.append(lc)
                         tline.append(tl2)
                         opindex.append(str(56))
                         op.append("push m")
                         opc.append("56D")
                 if sp1[i+1] in reg16:
                     indx=reg16.index(sp1[i+1])+1
                     tl1=l1.replace(sp1[i+1],"reg#"+str(indx)+"6")
                     tl2=tl1.replace(sp1[0],"op#"+str(57))
                     initaddr+=2
                     addr.append(initaddr)
                     line.append(l1)
                     lcnt.append(lc)
                     tline.append(tl2)
                     opindex.append(str(57))
                     op.append("push r16")
                     opc.append("57E")
             if(sp1[i]=="pop"):                 # pop instruction 
                 if sp1[i+1] in reg32:
                     indx=reg32.index(sp1[i+1])+1
                     tl1=l1.replace(sp1[i+1],"reg#"+str(indx)+"3")
                     tl2=tl1.replace(sp1[0],"op#"+str(58))
                     initaddr+=2
                     addr.append(initaddr)
                     line.append(l1)
                     lcnt.append(lc)
                     tline.append(tl2)
                     opindex.append(str(58))
                     op.append("pop r32")
                     opc.append("58F")
                 if(sp1[i+1].startswith("dword")):
                     k=sp1[1].split('[')
                     m=k[1].split(']')
                     if(m[0].isalpha()):
                         tl1=l1.replace(s[1],"sym#"+m[0])
                         tl2=tl1.replace(sp1[0],"op#"+str(59))
                         initaddr+=6
                         addr.append(initaddr)
                         line.append(l1)
                         lcnt.append(lc)
                         opindex.append(str(59))
                         op.append("pop m")
                         opc.append("59G")
                 if sp1[i+1] in reg16:
                     indx=reg16.index(sp1[i+1])+1
                     tl1=l1.replace(sp1[i+1],"reg#"+str(indx)+"6")
                     tl2=tl1.replace(sp1[0],"op#"+str(60))
                     initaddr+=2
                     addr.append(initaddr)
                     line.append(l1)
                     lcnt.append(lc)
                     tline.append(tl2)
                     opindex.append(str(60))
                     op.append("pop r16")
                     opc.append("60H")
             if sp1[i] in jmpint:            # jmp instruction
                 if(sp1[i+1]==sp2[i+2]):
                     indx=jmpint.index(sp1[i])+1
                     tl1=l1.replace(sp1[0],"op#"+str(i)+str(61))
                     tl2=tl1.replace(sp1[1],"sym#"+sp2[0])
                     initaddr+=2
                     addr.append(initaddr)
                     line.append(l1)
                     lcnt.append(lc)
                     tline.append(tl2)
                     opindex.append(str(i)+str(61))
                     op.append(sp1[i]+""+sp2[i+1])
                     opc.append(str(i)+"61I")
             if(sp1[i]=="mul"):              # mul instruction
                 if sp1[i+1] in reg32:
                     indx=reg32.index(sp1[i+1])+1
                     tl1=l1.replace(sp1[1],"reg#"+str(indx)+"3")
                     tl2=tl1.replace(sp1[0],"op#"+str(62))
                     initaddr+=2
                     addr.append(initaddr)
                     line.append(l1)
                     lcnt.append(lc)
                     tline.append(tl2)
                     opindex.append(str(62))
                     opc.append("62J")
                     op.append("mul r32")
                 elif sp1[i+1] in reg16:
                     indx=reg16.index(sp1[i+1])+1
                     tl1=l1.replace(sp1[1],"reg#"+str(indx)+"6")
                     tl2=tl1.replace(sp1[0],"op#"+str(63))
                     initaddr+=2
                     addr.append(initaddr)
                     line.append(l1)
                     lcnt.append(lc)
                     tline.append(tl2)
                     opindex.append(str(63))
                     opc.append("63K")
                     op.append("mul r16")
                 elif sp1[i+1] in reg8:
                     indx=reg8.index(sp1[i+1])+1
                     tl1=l1.replace(sp1[1],"reg#"+str(indx)+"8")
                     tl2=tl1.replace(sp1[0],"op#"+str(64))
                     initaddr+=2
                     addr.append(initaddr)
                     line.append(l1)
                     lcnt.append(lc)
                     tline.append(tl2)
                     opindex.append(str(64))
                     op.append("mul r8")
                     opc.append("64L")
             
             if(sp1[i]=="div"):  # div instruction 
                 if sp1[i+1] in reg32:
                     indx=reg32.index(sp1[i+1])+1
                     tl1=l1.replace(sp1[1],"reg#"+str(indx)+"3")
                     tl2=tl1.replace(sp1[0],"op#"+str(65))
                     initaddr+=2
                     addr.append(initaddr)
                     line.append(l1)
                     lcnt.append(lc)
                     tline.append(tl2)
                     opindex.append(str(65))
                     op.append("div r32")
                     opc.append("65M")
                 elif sp1[i+1] in reg16:
                     indx=reg16.index(sp1[i+1])+1
                     tl1=l1.replace(sp1[1],"reg#"+str(indx)+"6")
                     tl2=tl1.replace(sp1[0],"op#"+str(66))
                     initaddr+=2
                     addr.append(initaddr)
                     line.append(l1)
                     lcnt.append(lc)
                     tline.append(tl2)
                     opindex.append(str(66))
                     op.append("div r16")
                     opc.append("66N")
                 elif sp1[i+1] in reg8:
                     indx=reg8.index(sp1[i+1])+1
                     tl1=l1.replace(sp1[1],"reg#"+str(indx)+"8")
                     tl2=tl1.replace(sp1[0],"op#"+str(67))
                     initaddr+=2
                     addr.append(initaddr)
                     line.append(l1)
                     lcnt.append(lc)
                     tline.append(tl2)
                     opindex.append(str(67))
                     opc.append("67O")
                     op.append("div r8")            
             if(sp1[i]=="rep"):          # rep repne repe with string
                 if sp1[i+1] in strint32:   # instruction
                     tl1=l1.replace(l1,"op#"+str(i)+str(368))
                     initaddr+=2
                     addr.append(initaddr)
                     line.append(l1)
                     lcnt.append(lc)
                     tline.append(tl1)
                     opindex.append(str(i)+str(68))
                     op.append("rep "+strint32[i])
                     opc.append(str(i)+"68P")
             if(sp1[i]=="repe"):
                 if sp1[i+1] in strint32:
                     tl1=l1.replace(l1,"op#"+str(i)+str(369))
                     initaddr+=2
                     addr.append(initaddr)
                     line.append(l1)
                     lcnt.append(lc)
                     tline.append(tl1)
                     opindex.append(str(i)+str(69))
                     op.append("repe "+strint32[i])
                     opc.append(str(i)+"69Q")
             if(sp1[i]=="repne"):
                 if sp1[i+1] in strint32:
                     tl1=l1.replace(l1,"op#"+str(i)+str(370))
                     initaddr+=2
                     addr.append(initaddr)
                     line.append(l1)
                     lcnt.append(lc)
                     tline.append(tl1)
                     opindex.append(str(i)+str(70))
                     op.append("repne "+strint32[i])
                     opc.append(str(i)+"70R")
             if(sp1[i]=="rep"):
                 if sp1[i+1] in strint16:
                     tl1=l1.replace(l1,"op#"+str(i)+str(671))
                     initaddr+=2
                     addr.append(initaddr)
                     line.append(l1)
                     lcnt.append(lc)
                     tline.append(tl1)
                     opindex.append(str(i)+str(71))
                     op.append("rep "+strint16[i])
                     opc.append(str(i)+"71S")
             if(sp1[i]=="repe"):
                 if sp1[i+1] in strint16:
                     tl1=l1.replace(l1,"op#"+str(i)+str(672))
                     initaddr+=2
                     addr.append(initaddr)
                     line.append(l1)
                     lcnt.append(lc)
                     tline.append(tl1)
                     opindex.append(str(i)+str(72))
                     op.append("repe "+strint16[i])
                     opc.append(str(i)+"72T")
             if(sp1[i]=="repne"):
                 if sp1[i+1] in strint16:
                     tl1=l1.replace(l1,"op#"+str(i)+str(673))
                     initaddr+=2
                     addr.append(initaddr)
                     line.append(l1)
                     lcnt.append(lc)
                     tline.append(tl1)
                     opindex.append(str(i)+str(73))
                     op.append("repne "+strint16[i])
                     opc.append(str(i)+"73U")
             if(sp1[i]=="rep"):
                 if sp1[i+1] in strint8:
                     tl1=l1.replace(l1,"op#"+str(i)+str(874))
                     initaddr+=2
                     addr.append(initaddr)
                     line.append(l1)
                     lcnt.append(lc)
                     tline.append(tl1)
                     opindex.append(str(i)+str(74))
                     op.append("rep "+strint8[i])
                     opc.append(str(i)+"74V")
             if(sp1[i]=="repe"):
                 if sp1[i+1] in strint8:
                     tl1=l1.replace(l1,"op#"+str(i)+str(875))
                     initaddr+=2
                     addr.append(initaddr)
                     line.append(l1)
                     lcnt.append(lc)
                     tline.append(tl1)
                     opindex.append(str(i)+str(75))
                     op.append("repe "+strint8[i])
                     opc.append(str(i)+"75W")
             if(sp1[i]=="repne"):
                 if sp1[i+1] in strint8:
                     tl1=l1.replace(l1,"op#"+str(i)+str(876))
                     initaddr+=2
                     addr.append(initaddr)
                     line.append(l1)
                     lcnt.append(lc)
                     tline.append(tl1)
                     opindex.append(str(i)+str(76))
                     opc.append(str(i)+"76X")
                     op.append("repne "+strint8[i])
             if(sp1[i]=="cmp"):       #cmp instruction 
                 if sp1[i+1] in reg32:
                     s=sp1[i+1].split(",")
                     tl1=l1.replace(s[0],"reg#"+str(indx)+"3")
                     tl2=tl1.replace(s[1],"lit#"+s[1])
                     tl3=tl2.replace(sp1[0],"op#"+str(77))
                     initaddr+=2
                     addr.append(initaddr)
                     line.append(l1)
                     lcnt.append(lc)
                     tline.append(tl3)
                     opindex.append(str(77))
                     op.append("cmp r32,i")
                     opc.append("77Y")
                 if sp1[i+1] in reg16:
                     s=sp1[i+1].split(",")
                     tl1=l1.replace(s[0],"reg#"+str(indx)+"6")
                     tl2=tl1.replace(s[1],"lit#"+s[1])
                     tl3=tl2.replace(sp1[0],"op#"+str(78))
                     initaddr+=2
                     addr.append(initaddr)
                     line.append(l1)
                     lcnt.append(lc)
                     tline.append(tl3)
                     opindex.append(str(78))
                     op.append("cmp r16,i")
                     opc.append("78Z")
                 if sp1[i+1] in reg8:
                     s=sp1[i+1].split(",")
                     tl1=l1.replace(s[0],"reg#"+str(indx)+"8")
                     tl2=tl1.replace(s[1],"lit#"+s[1])
                     tl3=tl2.replace(sp1[0],"op#"+str(79))
                     initaddr+=2
                     addr.append(initaddr)
                     line.append(l1)
                     lcnt.append(lc)
                     tline.append(tl3)
                     opindex.append(str(79))
                     op.append("cmp r8,i")
                     opc.append("79A")
             if(sp1[i]=="call"):
                 if(sp1[i+1]=="printf"):
                     tl=l1.replace(sp1[0],"op#"+str(80))
                     tl1=tl.replace(sp1[1],str(""))
                     initaddr+=2
                     addr.append(initaddr)
                     line.append(l1)
                     lcnt.append(lc)
                     tline.append(tl1)
                     opindex.append(str(80))
                     op.append("call printf")
                     opc.append("80B")
                 
    lenline=len(tline)
    j=0
    for j in range(0,lenline):
        print(lcnt[j],end="    ")
        print(str(addr[j]).zfill(8),end="    ")
        print(line[j],end="    ")
        print(str(tline[j]))
        print()
        j+=1
                   
    fobj=open("literal.txt",'w')
    #fobj.write("lineNo"+"\t"+"litno "+" lit "+"\t"+"hex_conversion"+"\n")
    for i in range(len(lit)):
        fobj.write("\n"+str(lcnt[i])+"\t"+str(litcnt1[i])+"\t"+lit[i]+"\t"+hex(int(lit[i])))
    fobj2=open("register.txt","w")
    fobj2.write("register "+" value"+"\n")
    for i in range(len(reg32)):
        fobj2.write(reg32[i]+"  "+"\t"+str(reg32.index(reg32[i])+1)+"3"+"\n")
    for i in range(len(reg16)):
        fobj2.write(reg16[i]+"   "+"\t"+str(reg16.index(reg16[i])+1)+"6"+"\n")
    for i in range(len(reg8)):
        fobj2.write(reg8[i]+"   "+"\t"+str(reg8.index(reg8[i])+1)+"8"+"\n")
    fobj4=open("opc.txt","w")
    lis=[]
    for i in range(len(opindex)):
        if(lcnt[i] not in lis):
            lis.append(opindex[i])
            fobj4.write("op#"+opindex[i]+"\t"+opc[i]+"\n")
    fobj3=open("inter_code.txt","w")
    lst=[]
    #fobj3.write("\t Intermediate code\n\n" )
    for i in range(len(lcnt)):
            if lcnt[i] not in lst:
                lst.append(opindex[i])
                fobj3.write(str(i+1)+"\t"+str(lcnt[i])+"\t"+(str(addr[i]).zfill(8))+"\t"+tline[i]+" \n")
   

#inter_code("add2.asm","symbol.txt")


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
        c=cnt/2
    return c

           
            
def lst_code(f1,f2,f3,f4,f5,f6):
    reg32=["eax","ebx","ecx","edx","ebp","esp","esi","edi"]#32bit register
    reg16=["ax","bx","cx","dx"]#16bit register
    reg8=["ah","al","bh","bl","ch","cl","dh","dl"]#8bit register
    repint=["rep","repe","repne"]#rep instruction list
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
    fout=open("lst_op.txt","w")
    lcnt=0
    add1=0000000
    for ln1 in fn1:
        lcnt+=1
        #print(str(lcnt)+ln1)
        ls1=ln1.split()
        l1=len(ls1)
        if ls1==[]:
            fout.write(str(lcnt)+"\n")
        for i in range(l1):
           
            if(ls1[i]=="section" or ls1[i]=="global" or ls1[i]=="main:" or ls1[i]=="extern"):
                fout.write(str(lcnt)+"  "+"\t\t\t"+"\t\t"+str(ln1))
            if(ls1[i]=="dd"):
                for j in range(l2):
                    if ls1[i-1]==ls2[j]:
                        add=ls2[j+2]
                fout.write(str(lcnt)+"  "+str(add)+"\t"+str(replace_x(hex(int(ls1[i+1])))).zfill(8)+"\t\t"+str(ln1))
            if(ls1[i]=="db"):
                for j in range(l2):
                    if ls1[i-1]==ls2[j]:
                        add=ls2[j+2]
                fout.write(str(lcnt)+"  "+str(add)+"\t"+str(replace_x(hex(10)+hex(0))).zfill(8)+"\t\t"+str(ln1))
            if(ls1[i]=="resb"):
                for j in range(l2):
                    if ls1[i-1]==ls2[j]:
                        add=ls2[j+2]
                l=ls1[i+1]
                fout.write(str(lcnt)+"  "+str(add)+"\t"+" <res "+" "+str(replace_x(hex(int(l)))).zfill(8)+">"+"\t\t"+str(ln1))
            if(ls1[i]=="resd"):
                for j in range(l2):
                    if ls1[i-1]==ls2[j]:
                        add=ls2[j+2]
                l=int(ls1[i+1])*4
                fout.write(str(lcnt)+"  "+str(add)+"\t"+"<res "+" "+str(replace_x(hex(int(l)))).zfill(8)+">"+"\t\t"+str(ln1))
            if(ls1[i]=="mov"):  #for mov reg32,mem
                ls=ls1[i+1].split(",")
                if ls[1].startswith("dword"):
                    sp=ls1[1].split("[")
                    sp1=sp[1].split("]")
                    #print(sp1[0])
                    if(ls[0] in reg32 and sp1[0] in ls2):
                        for j in range(l2):
                            if sp1[0]==ls2[j]:
                                m=ls2[j+2]
                                #print(m)
                        for k in range(l5):
                            if str(lcnt)==ls5[k]:
                                n=ls5[k+2]
                                #print(n)
                        for x in range(l6):
                            if str(n)==ls6[x]:
                                l=ls6[x+1]
                        a=str(l)+'['+str(m)+']'
                        #print(a)
                        fout.write(str(lcnt)+"  "+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t"+str(ln1))
                        add1=add1+addr(a)
                if(ls[0] in reg32 and ls[1] in ls3): #for mov reg32,imm
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            m=ls3[j]
                            #print(m)
                    for k in range(l5):
                        if str(lcnt)==ls5[k]:
                            n=ls5[k+2]
                            #print(n)
                    for x in range(l6):
                        if(str(n)==ls6[x]):
                            l=ls6[x+1]
                            #print(l)
                    a=str(l)+'['+str(m).zfill(8)+']'
                    #print(a)
                    fout.write(str(lcnt)+"  "+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t\t"+str(ln1))
                    add1=add1+addr(a)
                if(ls[0] in reg32 and ls[1] in reg32): #mov reg32,reg32
                    for a in reg32:
                        if a==ls[0]:
                            x=a
                    for b in reg32:
                        if b==ls[1]:
                            x1=b
                    for k in range(l4):
                        if ls4[k]==x and ls4[k+1]==x1:
                            m=ls4[k+2]
                    for k in range(l5):
                        if str(lcnt-1) == ls5[k]:
                            n=ls5[k+2]
                    for x in range(l6):
                        if(n==ls6[x]):
                            l=ls6[x+1]
                    a=l+m
                    fout.write(str(lcnt)+"  "+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t\t"+str(ln1))
                    add1=add1+addr(a)
            if(ls1[i]=="add"):
                ls=ls1[i+1].split(",")
                # for add eax,ebx
                if(ls[0] in reg32 and ls[1] in reg32): 
                    for a in reg32:
                        if a==ls[0]:
                            x=a
                    for b in reg32:
                        if b==ls[1]:
                            x1=b
                    for k in range(l4):
                        if ls4[k]==x and ls4[k+1]==x1:
                            m=ls4[k+2]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            n=ls5[k+2]
                    for x in range(l6):
                        if(str(n)==ls6[x]):
                            l=ls6[x+1]
                    a=l+m
                    #print(a)
                    fout.write(str(lcnt)+"  "+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t\t"+str(ln1))
                    add1=add1+addr(a)
                if(ls[0] in reg32 and ls[1] in ls3):   #add reg32,imm
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            m=ls3[j]
                            #print(lcnt)
                    for k in range(l5):
                        if str(lcnt)==ls5[k]:
                            n=ls5[k+2]
                    for x in range(l6):
                        if(str(n)==ls6[x]):
                            l=ls6[x+1]
                    a=l+'['+m.zfill(8)+']'
                    #print(a)
                    fout.write(str(lcnt)+"  "+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t"+str(ln1))
                    add1=add1+addr(a)
                if(ls[0] in reg16 and ls[1] in reg16): #add reg16,reg16
                    for a in reg16:
                        if a==ls[0]:
                            x=a
                    for b in reg16:
                        if b==ls[1]:
                            x1=b
                    for k in range(l4):
                        if ls4[k]==x and ls4[k+1]==x1:
                            m=ls4[k+2]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            n=ls5[k+2]
                    for x in range(l6):
                        if(str(n)==ls6[x]):
                            l=ls6[x+1]
                    a=l+m
                    fout.write(str(lcnt)+"  "+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t"+str(ln1))
                    add1=add1+addr(a)
                if(ls[0] in reg16 and ls[1] in ls3): # add reg16,imm
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            m=ls3[j]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            n=ls5[k+2]
                    for x in range(l6):
                        if(n==ls6[x]):
                            l=ls6[x+1]
                    a=l+'['+m.zfill(8)+']'
                    fout.write(str(lcnt)+"  "+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t"+str(ln1))
                    add1=add1+addr(a)
            if(ls1[i]=="sub"):  #sub reg32,reg32
                ls=ls1[i+1].split(",")
                if(ls[0] in reg32 and ls[1] in reg32):
                    for a in reg32:
                        if a==ls[0]:
                            x=a
                    for b in reg32:
                        if b==ls[1]:
                            x1=b
                    for k in range(l4):
                        if ls4[k]==x and ls4[k+1]==x1:
                            m=ls4[k+2]
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            n=ls5[k+2]
                    for x in range(l6):
                        if(n==ls6[x]):
                            l=ls6[x+1]
                    a=l+m
                    fout.write(str(lcnt)+"  "+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t"+str(ln1))
                    add1=add1+addr(a)
                if(ls[0] in reg32 and ls[1] in ls3):   #sub reg32,imm
                    for j in range(l3):
                        if ls[1]==ls3[j]:
                            m=ls3[j]
                    for k in range(l5):
                        if str(lcnt)==ls5[k]:
                            n=ls5[k+2]
                    for x in range(l6):
                        if(n==ls6[x]):
                            l=ls6[x+1]
                    a=l+'['+m.zfill(8)+']'
                    fout.write(str(lcnt)+"  "+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t"+str(ln1))
                    add1=add1+addr(a)
            # jmp instruction
            if(ls1[i]=="jmp"):
                for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            m=ls5[k+2]
                for l in range(l6):
                    if str(m)==ls6[l]:
                        n=ls6[l+1]
                a=n
                fout.write(str(lcnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t"+str(ln1))
                add1=add1+addr(a)
            # mul  instruction
            if(ls1[i]=="mul"):
                if(ls1[i+1] in reg32 or ls1[i+1] in reg16 or ls1[i+1] in reg8):
                    print(ls1[i+1])
                    print(lcnt)
                    for k in range(l5):
                        if str(lcnt)==ls5[k]:
                            m=ls5[k+2]
                            #print(m)
                    for l in range(l6):
                        if str(m)==ls6[l]:
                            n=ls6[l+1]
                a=n
                fout.write(str(lcnt)+"  "+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t"+str(ln1))
                add1=add1+addr(a)
            # div instruction
            if(ls1[i]=="div"):
                for k in range(l5):
                        if str(lcnt-1) == ls5[k]:
                            m=ls5[k+2]
                for l in range(l6):
                    if str(m)==ls6[l]:
                        n=ls6[l+1]
                a=n+'F3'
                fout.write(str(lcnt)+"  "+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t"+str(ln1))
                add1=add1+addr(a)
            #inc instruction
            if(ls1[i]=='inc'):
                if(ls1[i+1] in reg32):
                    for k in range(l5):
                        if str(lcnt-1) == ls5[k]:
                            m=ls5[k+2]
                    for l in range(l6):
                        if str(m)==ls6[l]:
                            n=ls6[l+1]
                    a=n
                    fout.write(str(lcnt)+"  "+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t\t"+str(ln1))
                    add1=add1+addr(a)
                if(ls1[i+1] in reg16):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            m=ls5[k+2]
                    for l in range(l6):
                        if str(m)==ls6[l]:
                            n=ls6[l+1]
                    a=n
                    fout.write(str(lcnt)+"  "+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t"+str(ln1))
                    add1=add1+addr(a)
                if(ls1[i+1] in reg8):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            m=ls5[k+2]
                    for l in range(l6):
                        if str(m)==ls6[l]:
                            n=ls6[l+1]
                    a=n
                    fout.write(str(lcnt)+"  "+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t"+str(ln1))
                    add1=add1+addr(a)

            #dec instruction
            if(ls1[i]=='dec'):
                if(ls1[i+1] in reg32):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            m=ls5[k+2]
                    for l in range(l6):
                        if str(m)==ls6[l]:
                            n=ls6[l+1]
                    a=n
                    fout.write(str(lcnt)+"  "+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t"+str(ln1))
                    add1=add1+addr(a)
                if(ls1[i+1] in reg16):
                    for k in range(l5):
                        if strl(cnt) == ls5[k]:
                            m=ls5[k+2]
                    for l in range(l6):
                        if str(m)==ls6[l]:
                            n=ls6[l+1]
                    a=p1
                    fout.write(str(lcnt)+"  "+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t"+str(ln1))
                    add1=add1+addr(a)
                if(ls1[i+1] in reg8):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            m=ls5[k+2]
                    for l in range(l6):
                        if str(m)==ls6[l]:
                            n=ls6[l+1]
                    a=n
                    fout.write(str(lcnt)+"  "+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t"+str(ln1))
                    add1=add1+addr(a)

            if(ls1[i]=="xor"):
                ls=ls1[i+1].split(",")
                # for xor reg32,reg32
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
                            m=ls5[k+2]
                    for l in range(l6):
                        if str(m)==ls6[l]:
                            n=ls6[l+1]
                    a=n+s1
                    fout.write(str(lcnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t"+str(ln1))
                    add1=add1+addr(a)
                #for xor reg16,reg16
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
                            m=ls5[k+2]
                    for l in range(l6):
                        if str(m)==ls6[l]:
                            n=ls6[l+1]
                    a=n+s1
                    fout.write(str(lcnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t"+str(ln1))
                    add1=add1+addr(a)
                #for xor reg8,reg8
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
                            m=ls5[k+2]
                    for l in range(l6):
                        if str(m)==ls6[l]:
                            n=ls6[l+1]
                    a=n+s1
                    fout.write(str(lcnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t"+str(ln1))
                    add1=add1+addr(a)

            if(ls1[i]=="cmp"):
                ls=ls1[i+1].split(",")
                # for cmp reg32,reg32
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
                            m=ls5[k+2]
                    for l in range(l6):
                        if str(m)==ls6[l]:
                            n=ls6[l+1]
                    a=n+s1
                    fout.write(str(lcnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t"+str(ln1))
                    add1=add1+addr(a)
                #for cmp reg16,reg16
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
                            m=ls5[k+2]
                    for l in range(l6):
                        if str(m)==ls6[l]:
                            n=ls6[l+1]
                    a=n+s1
                    fout.write(str(lcnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t"+str(ln1))
                    add1=add1+addr(a)
                #for cmp reg8,reg8
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
                            m=ls5[k+2]
                    for l in range(l6):
                        if str(m)==ls6[l]:
                            n=ls6[l+1]
                    a=n+s1
                    fout.write(str(lcnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t"+str(ln1))
                    add1=add1+addr(a)
                #for cmp reg32,imm
                if(ls[0] in (reg32 or reg16 or reg8) and ls[1].isdigit()):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            m=ls5[k+2]
                    for l in range(l6):
                        if str(m)==ls6[l]:
                            n=ls6[l+1]
                    a=n+ls[1].zfill(2)
                    fout.write(str(lcnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t"+str(ln1))
                    add1=add1+addr(a)
            # je instruction
            if(ls1[i]=="je"):
                for k in range(l5):
                    if str(lcnt) == ls5[k]:
                        m=ls5[k+2]
                for l in range(l6):
                    if str(m)==ls6[l]:
                        n =ls6[l+1]
                a=n
                fout.write(str(lcnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t"+str(ln1))
                add1=add1+addr(a)
            # jz instruction
            if(ls1[i]=="jz"):
                for k in range(l5):
                    if str(lcnt) == ls5[k]:
                        m=ls5[k+2]
                for l in range(l6):
                    if str(m)==ls6[l]:
                        n=ls6[l+1]
                a=n
                fout.write(str(lcnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t"+str(ln1))
                add1=add1+addr(obj)
            # jne instruction
            if(ls1[i]=="jne"):
                for k in range(l5):
                    if str(lcnt) == ls5[k]:
                        m=ls5[k+2]
                for l in range(l6):
                    if str(m)==ls6[l]:
                        n=ls6[l+1]
                a=n
                fout.write(str(lcnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t"+str(ln1))
                add1=add1+addr(obj)
            # jg instruction
            if(ls1[i]=="jg"):
                for k in range(l5):
                    if str(lcnt) == ls5[k]:
                        m=ls5[k+2]
                for l in range(l6):
                    if str(m)==ls6[l]:
                        n=ls6[l+1]
                a=n
                fout.write(str(lcnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t"+str(ln1))
                add1=add1+addr(a)
            # jge instruction
            if(ls1[i]=="jge"):
                for k in range(l5):
                    if str(lcnt) == ls5[k]:
                        m=ls5[k+2]
                for l in range(l6):
                    if str(m)==ls6[l]:
                        n=ls6[l+1]
                a=n
                fout.write(str(lcnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t"+str(ln1))
                add1=add1+addr(a)
            # jl instruction
            if(ls1[i]=="jl"):
                for k in range(l5):
                    if str(lcnt) == ls5[k]:
                        m=ls5[k+2]
                for l in range(l6):
                    if str(m)==ls6[l]:
                        n=ls6[l+1]
                a=n
                fout.write(str(lcnt)+"  "+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t"+str(ln1))
                add1=add1+addr(a)
            # jle instruction
            if(ls1[i]=="jle"):
                for k in range(l5):
                    if str(lcnt) == ls5[k]:
                        m=ls5[k+2]
                for l in range(l6):
                    if str(m)==ls6[l]:
                        n=ls6[l+1]
                a=n
                fout.write(str(lcnt)+"  "+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t\t"+str(ln1))
                add1=add1+addr(a) 
            if ls1[i]=="push":    #push reg32
                if ls1[i+1] in reg32:
                    for k in range(l5):
                        if str(lcnt)==ls5[k]:
                            n=ls5[k+2]
                    for x in range(l6):
                        if(str(n)==ls6[x]):
                            l=ls6[x+1]
                    a=l
                    #print(a)
                    fout.write(str(lcnt)+"  "+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t\t"+str(ln1))
                    add1=add1+addr(a)
                #print(ls2)
                if(ls1[i+1] in ls2):  # push imm
                    for k in range(l2):
                        if ls2[k]==ls1[i+1]:
                            m=ls2[k+2]
                            #print(m)
                    for k in range(l5):
                        if str(lcnt-1) == ls5[k]:
                            n=ls5[k+2]
                    for x in range(l6):
                        if(n==ls6[x]):
                            l=ls6[x+1]
                    a=l+"["+m+"]"
                    fout.write(str(lcnt)+"  "+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t"+str(ln1))
                    add1=add1+addr(a)
            #call instruction
            if(ls1[i]=="call"):
                if(ls1[i+1]=="printf"):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            n=ls5[k+2]
                    for x in range(l6):
                        if(str(n)==ls6[x]):
                            l=ls6[x+1]
                            #print(l)
                    a=str(l)+'('+str(0).zfill(8)+')'
                    #print(a)
                    fout.write(str(lcnt)+"  "+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t"+str(ln1))
                    add1=add1+addr(a)
            if(ls1[i]=="call"):
                if(ls1[i+1]=="scanf"):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            n=ls5[k+2]
                            #print(n)
                    for x in range(l6):
                        if(str(n)==ls6[x]):
                            l=ls6[x+1]
                    a=l+'('+str(0).zfill(8)+')'
                    fout.write(str(lcnt)+"  "+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t"+str(ln1))
                    add1=add1+addr(a)
            if(ls1[i] in repint):
                if(ls1[i+1]=="movsb"):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            m=ls5[k+2]
                    for l in range(l6):
                        if str(p)==ls6[l]:
                            n=ls6[l+1]
                    a=n
                    fout.write(str(lcnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t"+str(ln1))
                    add1=add1+addr(a)
                elif(ls1[i+1]=="movsw"):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            m=ls5[k+2]
                    for l in range(l6):
                        if str(m)==ls6[l]:
                            n=ls6[l+1]
                    a=n
                    fout.write(str(lcnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t"+str(ln1))
                    add1=add1+addr(a)
                elif(ls1[i+1]=="movsd"):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            m=ls5[k+2]
                    for l in range(l6):
                        if str(m)==ls6[l]:
                            n=ls6[l+1]
                    a=n
                    fout.write(str(lcnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t"+str(ln1))
                    add1=add1+addr(a)
                elif(ls1[i+1]=="stosb"):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            m=ls5[k+2]
                    for l in range(l6):
                        if str(m)==ls6[l]:
                            n=ls6[l+1]
                    a=n
                    fout.write(str(lcnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t"+str(ln1))
                    add1=add1+addr(obj)
                elif(ls1[i+1]=="stosw"):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            m=ls5[k+2]
                    for l in range(l6):
                        if str(m)==ls6[l]:
                            n=ls6[l+1]
                    a=n
                    fout.write(str(lcnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t"+str(ln1))
                    add1=add1+addr(a)
                elif(ls1[i+1]=="stosd"):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            m=ls5[k+2]
                    for l in range(l6):
                        if str(m)==ls6[l]:
                            n=ls6[l+1]
                    a=n
                    fout.write(str(lcnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t"+str(ln1))
                    add1=add1+addr(a)
                elif(ls1[i+1]=="cmpsb"):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            m=ls5[k+2]
                    for l in range(l6):
                        if str(m)==ls6[l]:
                            n=ls6[l+1]
                    a=n
                    fout.write(str(lcnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t"+str(ln1))
                    add1=add1+addr(a)
                elif(ls1[i+1]=="cmpsw"):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            m=ls5[k+2]
                    for l in range(l6):
                        if str(m)==ls6[l]:
                            n=ls6[l+1]
                    a=n
                    fout.write(str(cnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t"+str(ln1))
                    add1=add1+addr(a)
                elif(ls1[i+1]=="cmpsd"):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            m=ls5[k+2]
                    for l in range(l6):
                        if str(m)==ls6[l]:
                            n=ls6[l+1]
                    a=n
                    fout.write(str(lcnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t"+str(ln1))
                    add1=add1+addr(a)
                
                elif(ls1[i+1]=="lodsb"):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            m=ls5[k+2]
                    for l in range(l6):
                        if str(m)==ls6[l]:
                            n=ls6[l+1]
                    a=n
                    fout.write(str(lcnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t"+str(ln1))
                    add1=add1+addr(a)
                elif(ls1[i+1]=="lodsw"):
                    for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            m=ls5[k+2]
                    for l in range(l6):
                        if str(m)==ls6[l]:
                            n=ls6[l+1]
                    a=n
                    fout.write(str(lcnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t"+str(ln1))
                    add1=add1+addr(a)
                else:
                    if(ls1[i+1]=="lodsd"):
                        for k in range(l5):
                            if str(lcnt) == ls5[k]:
                                m=ls5[k+2]
                        for l in range(l6):
                            if str(m)==ls6[l]:
                                n=ls6[l+1]
                        a=n
                        fout.write(str(lcnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t"+str(ln1))
                        add1=add1+addr(a)
            #std instruction
            if(ls1[i]=="std"):
                for k in range(l5):
                    if str(lcnt) == ls5[k]:
                        m=ls5[k+2]
                for l in range(l6):
                    if str(m)==ls6[l]:
                        n=ls6[l+1]
                a=n
                fout.write(str(lcnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t"+str(ln1))
                add1=add1+addr(a)
            #cld instruction
            if(ls1[i]=="cld"):
                for k in range(l5):
                        if str(lcnt) == ls5[k]:
                            m=ls5[k+2]
                for l in range(l6):
                    if str(m)==ls6[l]:
                        n=ls6[l+1]
                a=n
                fout.write(str(lcnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t"+str(ln1))
                add1=add1+addr(a)
            #ret instruction
            if(ls1[i]=="ret"):
                for k in range(l5):
                    if str(lcnt) == ls5[k]:
                        m=ls5[k+2]
                for l in range(l6):
                    if str(m)==ls6[l]:
                        n=ls6[l+1]
                a=n
                fout.write(str(lcnt)+"\t"+str(replace_x(hex(int(add1)))).zfill(8)+"\t"+str(a)+"\t\t"+str(ln1))
                add1=add1+addr(obj)
       

#lst_code("add2.asm","symbol.txt","literal.txt","mod.txt","inter_code.txt","opc.txt")

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

            


 #object_code("add2.asm","symbol.txt","literal.txt","mod.txt","inter_code.txt","newop.txt")

if __name__ == '__main__':
    a=argv[1]
    symtable(a)
    inter_code(a,"symbol.txt")
    lst_code(a,"symbol.txt","literal.txt","mod.txt","inter_code.txt","newop.txt")
    object_code(a,"symbol.txt","literal.txt","mod.txt","inter_code.txt","newop.txt")

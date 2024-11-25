import re
import fileout as fo
import random
class Dice:
    def do(s):
        e=Dice.spl(s)
        f=Dice.clean(e)
        if f==False:
            return False
        if f!=False:
            rs= Dice.calc(f)
        ss=str()
        sd=str()
        for i in rs[0]:
            ss+=str(i)
        for j in rs[2]:
            sd+=str(j)
        return ss,rs[1],rs[2]

    def spl(s):
        a=re.findall(r"\d+|\D",s)
        return a

    def clean(s):
        f=list()
        op=0
        cl=0
        for i in s:
            if f!=[]:
                if i.isdigit() and type(f[-1])!=int:
                    pass
                elif i=="d" and type(f[-1])==int:
                    pass
                elif i in "d+-*/" and f[-1]!="d+-*/":
                    pass
                elif i =="(":
                    op+=1
                elif i ==")":
                    op-=1
                    if op<0:
                        fo.printf("カッコがおかしいよ")
                        return False
                else:
                    fo.printf("入力がおかしいよ")
                    return False
            if i.isdigit():
                f.append(int(i))
            else:
                f.append(i)
        if op!=0:
            fo.printf("カッコの数がおかしいよ")
            return False
        return f

    def calc(sl):
        d,dlog=[],[]
        if "d" in sl:
            sl,dlog=Dice.dc(sl)
            d=sl.copy()
        if "(" in sl:
            sl=Dice.pri(sl)
        if "*" in sl or "/" in sl:
            sl=Dice.prd(sl)
        c=Dice.plm(sl)
        return d,c,dlog

    def roll(n,s):
        r=int()
        a=list()
        for i in range(n):
            a.append(random.randint(1,s))
        r=sum(a)
        return r,a

    def dc(sl):
        c=list()
        dlog=[]
        skip=0
        i=0
        while i<len(sl):
            if skip==1:
                skip=0
            elif sl[i]=="d":
                drs=Dice.roll(sl[i-1],sl[i+1])
                c[-1]=drs[0]
                dlog.append(drs[1])
                skip=1
            else:
                c.append(sl[i])
            i+=1
        return c,dlog

    def pri(sl):
        open=[]
        close=[]
        i=0
        c=list()
        while i<len(sl):
            if sl[i]=="(":
                open.append(i)
            elif sl[i]==")":
                close=i
                k=Dice.calc(sl[open.pop()+1:close])
                c.append(k[1])
            elif open==[]:
                c.append(sl[i])
            i+=1
        return c

    def prd(sl):
        i=0
        c=list()
        skip=0
        while i<len(sl):
            if skip==1:
                skip=0
                pass
            elif sl[i]=="*":
                c[-1]=c[-1]*sl[i+1]
                skip=1
            elif sl[i]=="/":
                c[-1]=c[-1]//sl[i+1]
                skip=1
            else:
                c.append(sl[i])
            i+=1
        return c

    def plm(sl):
        i=0
        c=int()
        j=None
        for i in sl:
            if type(i)==int:
                if j=="-":
                    j=i*-1
                else:
                    j=i
                c+=j
            j=i
        return c

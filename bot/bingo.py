from PIL import Image,ImageDraw,ImageFont
import shutil
import random
import os
POOL_PATH="pool.json"
def readf():
    file_data=open(POOL_PATH,"r").read().split("\n")
    return file_data
def resetf():
    open(POOL_PATH,"w").close()
def printf(s):
    open(POOL_PATH,"a").write(s+",")
def addf(s):
    open(POOL_PATH,"a").write(s+"\n")

def compression(nums:list) ->str:#数をaa~zzまでの文字列に変換し結合後、ランレングス
    result=[]
    for i in range(len(nums)):
        result.append(convert(nums[i]))
    return "".join(result)

def convert(num:int)->str: #数をaa~zzまでの文字列に変換
    result=[]
    alphabet="abcdefghijklmnopqrstuvwxyz"
    while len(result)<2:
        result.append(alphabet[num%26])
        num=num//26
    result.reverse()
    return "".join(result)

def runLength(s=str or list) -> str: #ランレングス圧縮
    l=len(s)
    result=[]
    if l==0:
        return result
    now=[s[0],0]
    for i in range(l):
        if s[i]==now[0]:
            now[1]+=1
        elif s[i]!=now[0]:#更新
            if now[1]==1:
                result.append(now[0])
            else:
                result.append("".join(map(str,now)))
            now=[s[i],1]
    if now[1]==1:
        result.append(now[0])
    else:
        result.append("".join(map(str,now)))
    return "".join(result)



def decode(key):
    alp = "abcdefghijklmnopqrstuvwxyz"
    return (alp.index(key[0])) * 26 + alp.index(key[1])


def card(numlist):
    return compression(numlist[:24])

def make_pool(min,max):
    numlist=[]
    for i in range(min,max+1):
        numlist.append(i)
    random.shuffle(numlist)
    resetf()
    register(numlist)
    return numlist

def register(numlist):
    resetf()
    for i in numlist:
        printf(str(i))

def set_reach(name,nums):
    readf()
    addf(str(name)+" "+str(nums))


def get_pool():
    try:
        file_data=readf()
        return file_data[0].split(",")[:-1]
    except FileNotFoundError:
        return ["まだ始まっていません！"]


def roll():
    try:
        file_data=readf()
        numlist=file_data[0].split(",")[:-1]
    except FileNotFoundError:
        return False
    if len(numlist)==0:
        return False
    result=numlist.pop()
    resetf()
    register(numlist)
    return result

def bingo(min,max):
    numlist=make_pool(min,max)
    numlist_temp=numlist.copy()
    shutil.copy(os.path.join("bingo.jpg"),os.path.join("work.jpg"))
    img=Image.open(os.path.join("work.jpg"))
    draw=ImageDraw.Draw(img)
    font=ImageFont.truetype(os.path.join("zenmaru.ttf"),80)
    pos=[60,205]
    for i in range(1,26):
        if i!=13:
            cell=str(numlist_temp.pop()).zfill(2)
            if len(cell)==3:
                draw.text((pos[0]-15,pos[1]),cell,"#FA7070",font=font)
            else:
                draw.text(tuple(pos),cell,"#A1C398",font=font)
        if 0<i:
            if i%5==0:
                pos[0]=60-130# 改行部分
                pos[1]+=130
            pos[0]+=130
    img.save(os.path.join("work.jpg"))
    return card(numlist[::-1])

if __name__=="__main__":
    print(bingo(1,75))




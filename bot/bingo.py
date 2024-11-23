from PIL import Image,ImageDraw,ImageFont
import shutil
import random
import os

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


def card(numlist):
    print(numlist[:24])
    return compression(numlist[:24])


def bingo(min,max):
    numlist=list()
    for i in range(min,max+1):
        numlist.append(i)
        random.shuffle(numlist)
    numlist_temp=numlist.copy()
    shutil.copy(os.path.join("bot","bingo.jpg"),os.path.join("bot","work.jpg"))
    img=Image.open(os.path.join("bot","work.jpg"))
    draw=ImageDraw.Draw(img)
    font=ImageFont.truetype(os.path.join("bot","zenmaru.ttf"),80)
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
    img.save(os.path.join("bot","work.jpg"))
    return card(numlist[::-1])

if __name__=="__main__":
    print(bingo(1,100))




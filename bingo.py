from PIL import Image,ImageDraw,ImageFont
import shutil
import random
def bingo(min,max):
    numlist=list()
    for i in range(min,max+1):
        numlist.append(i)
        random.shuffle(numlist)
    numlist_temp=numlist.copy()
    shutil.copy("bingo.jpg","work.jpg")
    img=Image.open("work.jpg")
    draw=ImageDraw.Draw(img)
    font=ImageFont.truetype("zenmaru.ttf",80)
    pos=[60,205]
    # cell=[(60,205),(182,205),(312,205),(442,205),(572,205),(52,335),(182,335),(312,335),(442,335),(572,335),(52,465),(182,465),(442,465),(572,465),(52,595),(182,595),(312,595),(442,595),(572,595),(52,725),(182,725),(312,725),(442,725),(572,725)]
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
    img.save("work.jpg")
    return numlist[::-1][:24]

if __name__=="__main__":
    bingo(1,100)




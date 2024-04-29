import discord
from discord import app_commands
import random
import re
import bingo
import datetime

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
                        print("カッコがおかしいよ")
                        return False
                else:
                    print("入力がおかしいよ")
                    return False
            if i.isdigit():
                f.append(int(i))
            else:
                f.append(i)
        if op!=0:
            print("カッコの数がおかしいよ")
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

with open("config.txt",mode="r",encoding="utf-8") as f:
    token=f.readline().split(":")
    token=token[1]
    status_message=f.readline().split(":")[1]

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

#起動
@client.event
async def on_ready():
    # アクティビティを設定
    new_activity = status_message
    await client.change_presence(activity=discord.Game(new_activity))
    # スラッシュコマンドを同期
    await tree.sync()

@client.event
async def on_voice_state_update(member, before, after):
    if before.channel == after.channel:
        return
    if not member == None:
        if before.channel!=None:
            await before.channel.send(member.display_name+"("+member.name+"が"+before.channel.name+"から退出しました")
        if after.channel!=None:
            await after.channel.send(member.display_name+"("+member.name+"が"+after.channel.name+"に入室しました")

@tree.command(name='r', description='ダイスを振るよ')
@app_commands.describe(input_dice="2d6 で6面ダイスを2回振るよ、後ろに+-*/()でかんたんな計算も出来るよ")
async def test(interaction: discord.Interaction,input_dice:str="1d100"):
    rs=Dice.do(input_dice)
    if rs==False:
        await interaction.response.send_message('入力がおかしいよ')
        return
    rd="# "+str(rs[1])+"\n``"+input_dice+"`` = "+" **"+str(rs[1])+"** ``"+"(="+rs[0]+")  <<"+str(rs[2])+"``"
    print(datetime.datetime.now(),interaction.user.name,"did \"/r\":",*rs)
    await interaction.response.send_message(rd)

@tree.command(name='ohuro', description='おふろのおんどは1d100度！')
async def test(interaction: discord.Interaction):
    rs=Dice.do("1d100")
    if rs==False:
        await interaction.response.send_message('入力がおかしいよ')
        return
    rd="# "+str(rs[1])+"度!"
    print(datetime.datetime.now(),interaction.user.name,"did \"/ohuro\":",*rs)
    await interaction.response.send_message(rd)

@tree.command(name='rs', description='シークレットダイスを振るよ')
@app_commands.describe(input_dice="2d6 で6面シークレットダイスを2回振るよ、後ろに+-*/()でかんたんな計算も出来るよ")
async def test(interaction: discord.Interaction,input_dice:str,):
    rs=Dice.do(input_dice)
    if rs==False:
        await interaction.response.send_message('入力がおかしいよ')
        return
    rd="# "+str(rs[1])+"\n``"+input_dice+"`` = "+" **"+str(rs[1])+"** ``"+"(="+rs[0]+")  <<"+str(rs[2])+"``"
    print(datetime.datetime.now(),interaction.user.name,"did \"/rs\":",*rs)
    await interaction.response.send_message(rd,ephemeral=True)

@tree.command(name='lit', description='(り・と・)って言うよ')
# @app_commands.describe(input_dice="2d6 で6面ダイスを2回振るよ、後ろに+-*/()でかんたんな計算も出来るよ")
async def test(interaction: discord.Interaction):
    print(datetime.datetime.now(),interaction.user.name,"did \"/lit\":")
    await interaction.response.send_message("(り・と・)っ")

@tree.command(name='lits', description='指定回数(り・と・)って言うよ、自分にしか見えないよ')
@app_commands.describe(count="2以上じゃないと動かないよ")
async def test(interaction: discord.Interaction,count:int):
    print(datetime.datetime.now(),interaction.user.name,"did \"/lits\":",count)
    if int(count)<2:
        await interaction.response.send_message('2以上じゃないと動かないよ',ephemeral=True)
        return
    else:
        await interaction.response.send_message("(り・と・)っ"*count,ephemeral=True)

@tree.command(name='choice', description='自分と同じ通話に居る人から一人メンションするよ')
# @app_commands.describe(count="通話に居てね")
async def test(interaction: discord.Interaction):
    print(datetime.datetime.now(),interaction.user.name,"did \"/choice\":")
    if interaction.user.voice==None:
        await interaction.response.send_message('通話に居てね')
        return
    else:
        v=interaction.user.voice.channel.members
        rl=list()
        for i in v:
            if i.bot==False:
                rl.append(i)
        r=random.choice(rl)
        await interaction.response.send_message(r.display_name+"("+r.name+")")

@tree.command(name='status', description='ステメ設定します')
@app_commands.describe(st="変更内容")
async def notice(interaction: discord.Interaction,st:str):
    print(datetime.datetime.now(),interaction.user.name,"did \"/status\":")
    global status_message
    status_message=st
    await client.change_presence(activity=discord.Game(st))
    await interaction.response.send_message(st+"に変更しました")

@tree.command(name='online', description='オンライン設定します')
@app_commands.describe(st="変更内容0:オンライン 1:退席中 2:取り込み中 3:オフライン")
async def notice(interaction: discord.Interaction,st:int):
    print(interaction.user.name,"did \"/online\":"+str(st))
    if st<0 or 3<st:
        await interaction.response.send_message('0~3の数値にしてね',ephemeral=True)
    else:
        if st==0 and client.status!=None:
            await interaction.response.send_message('オンラインに変更したよ!',ephemeral=True)
            # await client.change_presence(activity=discord.Game(status_message))
            await client.change_presence(status=discord.Status.online)
        elif st==1 and client.status!=discord.Status.idle:
            await interaction.response.send_message('退席中に変更したよ!',ephemeral=True)
            await client.change_presence(status=discord.Status.idle)
        elif st==2 and client.status!=discord.Status.dnd:
            await interaction.response.send_message('取り込み中に変更したよ!',ephemeral=True)
            await client.change_presence(status=discord.Status.dnd)
        elif st==3 and client.status!=discord.Status.offline:
            await interaction.response.send_message('オフラインに変更したよ!',ephemeral=True)
            await client.change_presence(status=discord.Status.offline)
        else:
            await interaction.response.send_message('前と一緒じゃない?',ephemeral=True)
        # await client.change_presence(activity=discord.Game(status_message))

@tree.command(name='syo', description='ハイ')
async def notice(interaction: discord.Interaction):
    print(datetime.datetime.now(),interaction.user.name,"did \"/syo\":")
    await interaction.response.send_message("ハイ")

@tree.command(name='bingo', description='ビンゴカードを出すよ')
async def notice(interaction: discord.Interaction):
    #とりま1~100まで固定
    bingo.bingo(1,100)
    print(datetime.datetime.now(),interaction.user.name,"did \"/bingo\"")
    await interaction.response.send_message(file=discord.File("work.jpg"))


client.run(token)

# while True:
#     text=input("ダイスを振るよ:")
#     rs=Dice.do(text)
#     rs=(text+"="+" **"+str(rs[1])+"** "+"(="+rs[0]+")")
#     print(rs)




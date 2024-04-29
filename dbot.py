import discord
from discord import app_commands
import random
import re
import bingo
import datetime
import nazotoki as nazo
# import nextcord
# from nextcord.ext import commands
# from nextcord import Interaction

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


# class Choose(discord.ui.Modal):
#     def __init__(self):
#         # questions=[]
#         data,ids=nazo.open_file()
#         questions=nazo.get_titles(data)
#         qs=[]
#         for i in questions:
#             qs.append(discord.SelectOption(label=i,value=i))
#         super().__init__(
#             title="謎解きフォーム",
#             timeout=None
#         )
        
#         self.answer = discord.ui.Select(
#             # label="問題を選んでね！",
#             placeholder="問題を選択:",
#             options=qs,
#             max_values=1,
#             # type=discord.ComponentType.select
#             # required=True
#         )
#         # self.add_item(self.answer)
#     async def on_submit(self, interaction: discord.Interaction) -> None:
#         return await interaction.response.send_message("あなたが入力したものはこれですね！\n"+self.answer.value)

# class Answer(discord.ui.Modal):
    def __init__(self):
        super().__init__(
            title="謎解きフォーム",
            timeout=None
        )
        
        self.answer = discord.ui.TextInput(
            label="答えを入力してね！",
            style=discord.TextStyle.short,
            placeholder="",
            required=True
        )
        self.add_item(self.answer)
    async def on_submit(self, interaction: discord.Interaction) -> None:
        return await interaction.response.send_message("あなたが入力したものはこれですね！\n"+self.answer.value)

class Question(discord.ui.Modal):
    def __init__(self):
        super().__init__(
            title="謎解きフォーム",
            timeout=None
        )
        
        self.question = discord.ui.TextInput(
            label="問題タイトルを入力してね！",
            style=discord.TextStyle.short,
            placeholder="",
            required=True
        )
        self.answer = discord.ui.TextInput(
            label="解答を入力してね！",
            style=discord.TextStyle.short,
            placeholder="",
            required=True
        )
        self.add_item(self.question)
        self.add_item(self.answer)
    async def on_submit(self, interaction: discord.Interaction) -> None:
            data,ids=nazo.open_file()
            rs=nazo.check_answer(self.question.value,self.answer.value,data)
            if rs==True:
                await interaction.response.send_message("ないす！ "+self.question.value+' 正解だよ',ephemeral=False)
            elif rs==False:
                await interaction.response.send_message('不正解だよ',ephemeral=True)
            else:
                await interaction.response.send_message('タイトルが見つかりませんでした、すまん',ephemeral=True)
    


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



## 以下コマンド

@tree.command(name='nazo', description='謎解き関連のコマンドだよ')
@app_commands.describe(command="add / remove / check",title="タイトル",answer="答え")
async def answer(interaction: discord.Interaction,command:str="check",title:str="",answer:str=""):
    print(datetime.datetime.now(),interaction.user.name,"did \"/nazo\":",command,title,answer)
    if command=="add":
        if title == "" or answer == "":
            await interaction.response.send_message('タイトルと答えを入力してね',ephemeral=True)
            return
        else:
            data,ids=nazo.open_file()
            suc,data,ids=nazo.add_contents(title,answer,data,ids)
            if suc:
                nazo.write_file(data)
                await interaction.response.send_message("**"+title+"**というタイトルの謎解きの答えを**"+answer+"**として覚えたよ！",ephemeral=True)
            else:
                await interaction.response.send_message('タイトルが被っています',ephemeral=True)
    elif command=="remove":
        if title == "":
            await interaction.response.send_message('タイトルを入力してね',ephemeral=True)
            return
        else:
            data,ids=nazo.open_file()
            suc,data,ids=nazo.remove_contents(title,data,ids)
            if suc:
                nazo.write_file(data)
                await interaction.response.send_message("1..2の...ポカン！**"+title+"**というタイトルの謎解きの答えをきれいさっぱり忘れたよ！",ephemeral=True)
            else:
                await interaction.response.send_message('タイトルが見つかりませんでした、すまん',ephemeral=True)
    elif command=="check":
        if title == "" or answer == "":
            await interaction.response.send_modal(Question())
            # await interaction.response.send_modal(Answer())
        else:
            data,ids=nazo.open_file()
            rs=nazo.check_answer(title,answer,data)
            if rs==True:
                await interaction.response.send_message('正解だよ',ephemeral=False)
            elif rs==False:
                await interaction.response.send_message('不正解だよ',ephemeral=True)
            else:
                await interaction.response.send_message('タイトルが見つかりませんでした、すまん',ephemeral=True)









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


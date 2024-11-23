import discord
from discord import app_commands
import random
import re
import bingo
import nazotoki as nazo
import fileout as fo
import os

def is_prime(n):
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True
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
def check_answer(title:str,answer:str,user:str):
    data,ids=nazo.open_file()
    rs=nazo.check_answer(title,answer,data)
    if rs==True:
        return user+" "+"ないす！ "+title+" "+"  →"+' 正解だよ',False,discord.ui.View()
    elif rs==False:
        return user+" "+title+" "+answer+"  →"+':不正解だよ',True,setanswer(title)
class Answer(discord.ui.Modal):
    def __init__(self,title:str):
        super().__init__(
            title=title,
            timeout=None
        )
        self.answer = discord.ui.TextInput(
            label="解答を入力してね！",
            style=discord.TextStyle.short,
            placeholder="",
            required=True
        )
        self.add_item(self.answer)
    async def on_submit(self, interaction: discord.Interaction) -> None:
        fo.printf(interaction.user.name,"did \"modal\":","check",self.title,self.answer.value)
        return_message,em,v=check_answer(self.title,self.answer.value,interaction.user.mention)
        await interaction.response.send_message(return_message,ephemeral=em,view=v)
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
        fo.printf(interaction.user.name,"did \"/nazo\":","check",self.question.value,self.answer.value)
        return_message,em,v=check_answer(self.title,self.answer.value,interaction.user.mention)
        await interaction.response.send_message(return_message,ephemeral=em,view=v)
def setbutton(title:str):
    button = discord.ui.Button(label=title+"にこたえる！",style=discord.ButtonStyle.success,custom_id=title)
    view = discord.ui.View()
    view.add_item(button)
    return view
def setanswer(title:str,turn=False):
    if turn:
        button = discord.ui.Button(label="あきらめて答えを見る",style=discord.ButtonStyle.danger,custom_id="!"+title)
    else:
        button = discord.ui.Button(label=title+"の答えを見る",style=discord.ButtonStyle.secondary,custom_id="?"+title)
    view = discord.ui.View()
    view.add_item(button)
    return view
class QuestionAdd(discord.ui.Modal):
    def __init__(self):
        super().__init__(
            title="謎解き追加フォーム",
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
            fo.printf(interaction.user.name,"did \"modal\":","add",self.question.value,self.answer.value)
            data,ids=nazo.open_file()
            suc,data,ids=nazo.add_contents(self.question.value,self.answer.value,data,ids)
            if suc:
                nazo.write_file(data)
                await interaction.response.send_message("",view=setbutton(self.question.value),ephemeral=False)
            else:
                await interaction.response.send_message('タイトルが被っています',ephemeral=True)
            # fo.printf(interaction.user.name,"did \"/nazo\":","add",self.question.value,self.answer.value)
def getAnswer(title):
    c=nazo.open_file()
    return nazo.get_answer(title,c[0])
with open(os.path.join("config.txt"),mode="r",encoding="utf-8") as f:
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
    fo.printf("Bot","is ready")
    await client.change_presence(activity=discord.Game(new_activity))
    # スラッシュコマンドを同期
    await tree.sync()

#全てのインタラクションを取得
@client.event
async def on_interaction(interaction:discord.Interaction):
    try:
        if interaction.data['component_type'] == 2:
            await on_button_click(interaction)
    except KeyError:
        pass

## Buttonの処理
async def on_button_click(interaction:discord.Interaction):
    fo.printf(interaction.user.name,"did \"Interaction\":",interaction.data["custom_id"])
    custom_id = interaction.data["custom_id"]
    #ここから下に書く
    if custom_id[0]=="!":
        title=custom_id[1:]
        await interaction.response.send_message(title+"の答えは:**"+getAnswer(title)+"**でした！！",ephemeral=True)    
    elif custom_id[0]=="?":
        await interaction.response.send_message("## 答え出すけどいい？\nもし、いらない場合は右下の これらのメッセージを削除するを押してね。↓",view=setanswer(custom_id[1:],True),ephemeral=True)
    else:
        c=nazo.open_file()
        titles=set(nazo.get_titles(c[0]))
        if custom_id in titles:
            await interaction.response.send_modal(Answer(custom_id))
        else:
            await interaction.response.send_message("問題が削除されたか、未登録かも！りっとーに助けを求めてね",ephemeral=True)
@client.event
async def on_voice_state_update(member, before, after):
    if before.channel == after.channel:
        return
    if not member == None:
        if before.channel!=None:
            await before.channel.send(member.display_name+"("+member.name+"が"+before.channel.name+"から退出しました")
        if after.channel!=None:
            await after.channel.send(member.display_name+"("+member.name+"が"+after.channel.name+")に入室しました")

## 以下コマンド

@tree.command(name='nazo', description='謎解き関連のコマンドだよ')
@app_commands.describe(command="add / remove / check / set",title="タイトル",answer="答え")
async def answer(interaction: discord.Interaction,command:str="check",title:str="",answer:str=""):
    fo.printf(interaction.user.name,"did \"/nazo\":",command,title,answer)
    if command=="add":
        if title == "" or answer == "":
            await interaction.response.send_modal(QuestionAdd())
            return
        else:
            data,ids=nazo.open_file()
            suc,data,ids=nazo.add_contents(title,answer,data,ids)
            if suc:
                nazo.write_file(data)
                await interaction.response.send_message("",view=setbutton(title),ephemeral=False)
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
        else:
            fo.printf(interaction.user.name,"did \"modal\":","check",title,answer)
            return_message,em,v=check_answer(title,answer,interaction.user.mention)
            await interaction.response.send_message(return_message,ephemeral=em,view=v)
    else:
        await interaction.response.send_message('コマンドがおかしいよ',ephemeral=True)

@tree.command(name='r', description='ダイスを振るよ')
@app_commands.describe(input_dice="2d6 で6面ダイスを2回振るよ、後ろに+-*/()でかんたんな計算も出来るよ")
async def test(interaction: discord.Interaction,input_dice:str="1d100"):
    rs=Dice.do(input_dice)
    fo.printf(interaction.user.name,"did \"/r\":",*rs)
    if rs==False:
        await interaction.response.send_message('入力がおかしいよ')
        return
    rd="# "+str(rs[1])+"\n``"+input_dice+"`` = "+" **"+str(rs[1])+"** ``"+"(="+rs[0]+")  <<"+str(rs[2])+"``"
    await interaction.response.send_message(rd)

@tree.command(name='ohuro', description='おふろのおんどは1d100度！')
async def test(interaction: discord.Interaction):
    rs=Dice.do("1d100")
    fo.printf(interaction.user.name,"did \"/ohuro\":",*rs)
    if rs==False:
        await interaction.response.send_message('入力がおかしいよ')
        return
    rd="# "+str(rs[1])+"度!"
    await interaction.response.send_message(rd)

@tree.command(name='rs', description='シークレットダイスを振るよ')
@app_commands.describe(input_dice="2d6 で6面シークレットダイスを2回振るよ、後ろに+-*/()でかんたんな計算も出来るよ")
async def test(interaction: discord.Interaction,input_dice:str):
    rs=Dice.do(input_dice)
    fo.printf(interaction.user.name,"did \"/rs\":",*rs)
    if rs==False:
        await interaction.response.send_message('入力がおかしいよ')
        return
    rd="# "+str(rs[1])+"\n``"+input_dice+"`` = "+" **"+str(rs[1])+"** ``"+"(="+rs[0]+")  <<"+str(rs[2])+"``"
    await interaction.response.send_message(rd,ephemeral=True)

@tree.command(name='lit', description='(り・と・)って言うよ')
async def test(interaction: discord.Interaction):
    fo.printf(interaction.user.name,"did \"/lit\":")
    await interaction.response.send_message("(り・と・)っ")

@tree.command(name='lits', description='指定回数(り・と・)って言うよ、自分にしか見えないよ')
@app_commands.describe(count="2以上じゃないと動かないよ")
async def test(interaction: discord.Interaction,count:int):
    fo.printf(interaction.user.name,"did \"/lits\":",count)
    if int(count)<2:
        await interaction.response.send_message('2以上じゃないと動かないよ',ephemeral=True)
        return
    else:
        await interaction.response.send_message("(り・と・)っ"*count,ephemeral=True)

@tree.command(name='prime', description='素数かどうか教えてくれるよ！')
@app_commands.describe(count="整数を入力してね")
async def test(interaction: discord.Interaction,count:int):
    fo.printf(interaction.user.name,"did \"/prime\":",count)
    if count==57:
        await interaction.response.send_message("# **57は素数だよ！**\n誰がなんと言おうとも、57は素数だよ！")
        return
    elif is_prime(count):
        await interaction.response.send_message(str(count)+"は素数だよ！")
    else:
        await interaction.response.send_message(str(count)+"は素数ではないよ！！")

@tree.command(name='choice', description='自分と同じ通話に居る人から一人メンションするよ')
async def test(interaction: discord.Interaction):
    fo.printf(interaction.user.name,"did \"/choice\":")
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

@tree.command(name='syo', description='ハイ')
async def notice(interaction: discord.Interaction):
    fo.printf(interaction.user.name,"did \"/syo\":")
    await interaction.response.send_message("ハイ")


@tree.command(name='67', description='そんなぁ！')
async def notice(interaction: discord.Interaction):
    fo.printf(interaction.user.name,"did \"/67\":")
    await interaction.response.send_message("そんなぁ！")


@tree.command(name='bingo', description='ビンゴカードを出すよ')
async def notice(interaction: discord.Interaction):
    fo.printf(interaction.user.name,"did \"/bingo\"")
    #とりま1~100まで固定
    num_list=bingo.bingo(1,100)
    await interaction.response.defer(thinking=True)
    # await interaction.followup.send(str(num_list).replace(" ",""))
    await interaction.followup.send("[ビンゴカードを開く](https://lit-to.github.io/tadabot/index.html?card="+str(num_list)+"&?name="+interaction.user.display_name+")")
    await interaction.followup.send(file=discord.File(os.path.join("bot","work.jpg")))

@tree.command(name='exit', description='ばいばーい')
async def exits(interaction: discord.Interaction):
    fo.printf(interaction.user.name,"did \"/exit\":")
    if interaction.user.id==int(379155307546542081):
        await interaction.response.send_message("ばいばーい",ephemeral=True)
        await client.close()
    else:
        await interaction.response.send_message("あぶない！このコマンドはサーバーが爆発します！<@!712105359673917480> を呼んでね")

@tree.command(name='status', description='通話ステータスを変更するよ')
@app_commands.describe(color="1:赤 2:黄 3:青",input_status="後ろの説明書きを入力してね")
async def test(interaction: discord.Interaction,color:int=-1,input_status:str=""):
    fo.printf(interaction.user.name,"did \"/status\":")
    statusChannel=interaction.guild.get_channel(1268210484499447828)
    if color==-1:
        status=statusChannel.name[0]
    elif color==1:
        status="🔴"
    elif color==2:
        status="🟡"
    elif color==3:
        status="🔵"
    if status=="":
        status+=statusChannel.name[1:]
    else:
        status+=input_status
    await statusChannel.edit(name=status,reason="status changed by "+interaction.user.name)
    await interaction.response.send_message("ステータスを変更しました",ephemeral=True)
    return

@tree.command(name='lock', description='今入っている通話のロックをかけるか、外せるよ')
async def test(interaction: discord.Interaction):
    fo.printf(interaction.user.name,"did \"/lock\":")
    if interaction.user.voice==None:
        await interaction.response.send_message('通話に居てね',ephemeral=True)
        return
    else:
        if (interaction.user.voice.channel.permissions_for(interaction.user).connect):
            await interaction.user.voice.channel.set_permissions(interaction.guild.default_role,connect=False)
            await interaction.response.send_message(interaction.user.voice.channel.name+"をロックしました",ephemeral=False)
            return
        else:
            await interaction.user.voice.channel.set_permissions(interaction.guild.default_role,connect=True)
            await interaction.response.send_message(interaction.user.voice.channel.name+"のロックを解除しました",ephemeral=False)
            return






























client.run(token)

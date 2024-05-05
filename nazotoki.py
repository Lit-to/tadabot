import csv
path="answers.csv"

def open_file(path="answers.csv"):
    with open(path,mode="r",encoding="UTF-8") as f:
        reader=csv.reader(f)
        contents=[]
        for row in reader:
            contents.append(row)
        titles=set()
        for i in contents:
            if len(i)==2:
                titles.add(i[0])
        return contents,titles

def write_file(contents,path="answers.csv"):
    with open(path,mode="w",encoding="UTF-8",newline="") as f:
        writer=csv.writer(f)
        for row in contents:
            writer.writerow(row)

def add_contents(title,answer,contents,titles):
    if title in titles or 0<title.count(" "):
        return False,contents,titles
    contents.append([title,answer])
    titles.add(title)
    return True,contents,titles


def remove_contents(title,contents,titles):
    for i in range(len(contents)):
        if contents[i][0]==title:
            contents.pop(i)
            titles.remove(title)
            return True,contents,titles
    return False,contents,titles

def show_contents(contents):
    for i in range(len(contents)):
        print(contents[i][0],":",contents[i][1])
    return contents

def check_answer(title,answer,contents):
    for i in range(len(contents)):
        if contents[i][0]==title:
            if contents[i][1]==answer:
                return True
            else:
                return False
    return -1

def get_titles(contents):
    titles=[]
    for i in range(len(contents)):
        titles.append(contents[i][0])
    return titles

def get_answer(title,contents):
    for i in range(len(contents)):
        if contents[i][0]==title:
            return contents[i][1]
    return False

s=[]
data,ids=open_file(path)
# while s!=["exit"]:
#     s=input().split()
#     if s[0]=="add":
#         if len(s)!=3:
#             print("wrong arguments!")
#             s=[s[0],"",""]
#             s[1]=(input("title:"))
#             s[2]=(input("answer:"))
#         if len(s)==3:
#             suc,data,ids=add_contents(s[1],s[2],data,ids)
#             if suc:
#                 write_file(path,data)
#                 print(s[1],s[2],"added")
#             else:
#                 print("title already exists")
#     elif s[0]=="remove":
#         if len(s)!=2:
#             print("wrong arguments!")
#             s=[s[0],""]
#             s[1]=(input("title:"))
#         if len(s)==2:
#             suc,data,ids=remove_contents(s[1],data,ids)
#             if suc:
#                 write_file(path,data)
#                 print(s[1],"removed")
#             else:
#                 print("title is not exists")
#     elif s[0]=="check":
#         if len(s)!=3:
#             print("wrong arguments!")
#             s=[s[0],"",""]
#             s[1]=(input("title:"))
#             s[2]=(input("answer:"))
#         if len(s)==3:
#             if check_answer(s[1],s[2],data)==True:
#                 print("correct!")
#             elif check_answer(s[1],s[2],data)==False:
#                 print("incorrect!")
#             else:
#                 print("title is not exists or include half space")
#     elif s[0]=="show":
#         show_contents(data)
#     elif s[0]=="save":
#         write_file(path,data)
#         print("saved")
#     elif s[0]=="exit":
#         print("bye")
#         break
#     elif s[0]=="reload":
#         data,ids=open_file(path)
#         print("reloaded!")
#     elif s[0]=="reset":
#         if input("are you sure? (yes/no)")=="yes":
#             data=[]
#             ids=set()
#             data,ids=open_file(path)
#             print("reseted!")
#     elif s[0]=="help":
#         print("add [title] [answer]: add new answer")
#         print("remove [title]: remove answer")
#         print("check [title] [answer]: check answer")
#         print("show: show all answers")
#         print("save: save answers")
#         print("exit: exit")
#         print("reload: reload answers")
#         print("reset: reset answers")
# write_file(path,data)




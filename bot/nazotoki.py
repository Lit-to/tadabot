import csv
import os
path=os.path.join("answers.csv")

def open_file(path=path):
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

def write_file(contents,path=path):
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

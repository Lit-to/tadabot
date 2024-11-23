import datetime

def printf(*args):
    print(datetime.datetime.now(),*args)
    with open('../log.txt', 'a',encoding="utf-8") as f:
        print(datetime.datetime.now(),*args,file=f)
    # print(datetime.datetime.now(),*args,file=open('./log.txt', 'a',encoding="utf-8").close())

# printf('hello world')



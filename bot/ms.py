import subprocess, sys


def getMsInfo():
    option = ""
    if 1 < len(sys.argv):
        option = sys.argv[1]
    subprocess.Popen(["D:\\ssn\\start.bat"])
    config = open("msConfig.txt", "r").readlines()
    if option == "key":
        print("\n".join(config))
    else:
        print(config[0])

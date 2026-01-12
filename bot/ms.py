import subprocess, sys


def getMsInfo(key, server):
    subprocess.Popen(["D:\\ssn\\start.bat"])
    config = open("msConfig.txt", "r").readlines()
    if key == "True":
        print("\n".join(config))
    else:
        print(config[0])
    if server == "True":
        subprocess.Popen(["E:\\minecraft\\server\\tkp2026\\start.bat"])

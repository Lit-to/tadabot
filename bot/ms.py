import subprocess


def getMsInfo(key, server):
    subprocess.Popen(["D:\\ssn\\start.bat"])
    config = open("msConfig.txt", "r", encoding="utf-8").readlines()
    result = []
    if server == "True":
        subprocess.Popen(["E:\\minecraft\\server\\tkp2026\\start.bat"])
        result.append("サーバーを起動中です！少々お待ちください。")
    if key == "True":
        result.append(config[0])
        result.append(config[1])
    else:
        result.append(config[0])
    return "\n".join(result)

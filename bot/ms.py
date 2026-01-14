import subprocess
import time
import re


def getMsInfo(key, server):
    subprocess.Popen(
        ["D:\\ssn\\start.bat"], creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    config = open("msConfig.txt", "r", encoding="utf-8").readlines()
    result = []
    if server == "True":
        subprocess.Popen(
            ["E:\\minecraft\\server\\tkp2026\\start.bat"],
            creationflags=subprocess.CREATE_NEW_CONSOLE,
        )
    time.sleep(5)
    ipinfo = open("D:\\ssn\\output.log", mode="r", encoding="utf-8").read()
    if key == "True":
        result.append(config[0])
        urls = re.findall(r"(https?://[^\s]+)", ipinfo)
        if urls:
            result.append(urls[-1])
        else:
            result.append("IP情報の取得に失敗しました。")
        result.append(config[1])
    else:
        result.append(config[0])
    return "\n".join(result)

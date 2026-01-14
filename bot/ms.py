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

    if key == "True":
        result.append(config[0])
        result.append(config[1])
    else:
        result.append(config[0])

    ipinfo = open("D:\\ssn\\output.log", mode="r", encoding="utf-8").read()
    urls = re.findall(r"(https?://[^\s]+)", ipinfo)
    if urls:
        result.append(urls[-1].strip())
    else:
        result.append("IP情報の取得に失敗しました。")

    return "\n".join(result)

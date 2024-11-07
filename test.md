[Unit]
Description=ping service
After=network.target

[Service]
User=root
ExecStart=/home/bot/tadabot/tadabot/start.sh
Restart=always

[Install]
WantedBy=multi-user.target

--
cd /bot/tadabot/tadabot
. ../bin/activate
python3 dbot.py
deactivate

ls -la | awk 'NR>1{cmd="stat "$NF" -c %a";cmd|getline c;close(cmd);print c,$0}'


 auto_load.service: Failed to execute /home/bot/tadabot/tadabot/start.sh: Exec format error
 cd /etc/systemd/system/

サービスファイルの冒頭に``#!/bin/bash``が必要！！

https://qiita.com/vukujin/items/68d0957d7ac3c1dec977




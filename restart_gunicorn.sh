#!/bin/bash
ps aux|grep settings.py|awk '{print $2}'|xargs kill -9
sleep 1.5

# 开启操作系统最大代开文件数
# ulimit -n 65535

#切到flask项目根目录下，使用该行命令启动flask项目，也可以使用sh restart_gunicorn.sh进行启动flask项目
gunicorn -c settings.py main:app
ps aux|grep settings.py|head -3
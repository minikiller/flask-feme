from flask_restful import Resource
from flask import request, jsonify, make_response
import json
from flask_jwt import jwt_required, current_identity
import os
import subprocess


# 读取配置文件site.ini，用来配置进程名，程序包版本名
import configparser
config = configparser.ConfigParser()
filename=config.read('/Users/mclitao/Project/6666-admin/flask-feme/app/resources/site.ini',encoding='utf-8')
print(filename)

secs=config.sections()
sec = config.options("SHELLCLI")

MD_Name=config.get('SHELLCLI','MD_Name')
ME_Name=config.get('SHELLCLI','ME_Name')
MD_jar=config.get('SHELLCLI','MD_jar')
ME_jar=config.get('SHELLCLI','ME_jar')
MD_jar_path=config.get('SHELLCLI','MD_jar_path')
ME_jar_path=config.get('SHELLCLI','ME_jar_path')


PS_EF_MD='ps -ef |grep \'java -cp\' |grep ' + MD_Name + '|wc -l'
PS_EF_ME='ps -ef |grep \'java -cp\' |grep '+ ME_Name + ' |wc -l'

Start_MD='nohup java -cp  ' + MD_jar_path + ' quickfix.examples.executor.MarketDataServer'
Stop_MD='ps -ef |grep ' + MD_jar + ' |awk \'{print $2}\'| grep -v grep |xargs kill -15'
_Stop_MD='ps -ef |grep ' + MD_jar + ' |awk \'{print $2}\' |wc -l'

Start_ME='nohup java -cp ' + ME_jar_path + ' quickfix.examples.ordermatch.MatchingEngine'
Stop_ME='ps -ef |grep ' + ME_jar + ' |awk \'{print $2}\'| grep -v grep |xargs kill -15'
_Stop_ME='ps -ef |grep ' + ME_jar + ' |awk \'{print $2}\' |wc -l'


"""
服务器脚本命令

PS_EF_MD='ps -ef |grep \'java -cp\' |grep quickfix.examples.executor.MarketDataServer |wc -l'
PS_EF_ME='ps -ef |grep \'java -cp\' |grep quickfix.examples.ordermatch.MatchingEngine |wc -l'

Start_MD='nohup java -cp  /Users/mclitao/Project/9999-futures/ccme/marketdata/target/ccme-marketdata-2.2.0-standalone.jar quickfix.examples.executor.MarketDataServer'
Stop_MD='ps -ef |grep ccme-marketdata-2.2.0-standalone |awk \'{print $2}\'| grep -v grep |xargs kill -15'
_Stop_MD='ps -ef |grep ccme-marketdata-2.2.0-standalone |awk \'{print $2}\' |wc -l'

Start_ME='nohup java -cp ~/Project/9999-futures/ccme/matchingengine/target/ccme-mathcingengine-2.2.0-standalone.jar  quickfix.examples.ordermatch.MatchingEngine'
Stop_ME='ps -ef |grep ccme-mathcingengine-2.2.0-standalone |awk \'{print $2}\'| grep -v grep |xargs kill -15'
_Stop_ME='ps -ef |grep ccme-mathcingengine-2.2.0-standalone |awk \'{print $2}\' |wc -l'


MD服务端口
 mclitao@TaodeMacBook-Pro  ~  lsof -i :9880
COMMAND   PID    USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
java    49321 mclitao   55u  IPv6 0x3eacc9edad364093      0t0  TCP *:9880 (LISTEN)


ME服务端口
 mclitao@TaodeMacBook-Pro  ~  lsof -i :8323
COMMAND   PID    USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
java    49290 mclitao   49u  IPv6 0x3eacc9edad365913      0t0  TCP *:8323 (LISTEN)

"""



#负责执行CLI命令,并返回结果
def exec_cli(_cmd):
    try:
        #os.system：获取程序执行命令的返回值。
        #os.popen： 获取程序执行命令的输出结果。
        print(_cmd)
        val = os.popen(_cmd)
        out = val.read()
    except:
        out = 'Error'
        print('exec shell stript Error!!')

    return out
#处理掉特殊字符
def change_str(out):
    _str_s=out.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
    return _str_s

#列出服务
class ListService(Resource):
    # @jwt_required()
    def get(self):

        # MD服务检查'
        mdout=exec_cli(PS_EF_MD)
        try:
            if int(mdout)>1 :
                _mdStatus=1
            else:
                _mdStatus=0
        except:
                _mdStatus=0

        # ME服务检查
        meout=exec_cli(PS_EF_ME)
        # print(meout)
        try:
            if int(meout)>1 :
                _meStatus=1
            else:
                _meStatus=0
        except:
                _meStatus=0

        # 返回2个服务的真实状态   
        return jsonify({'MD':_mdStatus,"ME":_meStatus})
        
#启动MD
class MDStartService(Resource):
    # @jwt_required()
    """
       java启动 必须已cp参数启动不然后面ps -ef 查不到这个进程
    """
    def get(self):
        #检查是否已经启动过
        out=exec_cli(PS_EF_MD)
        print(int(change_str(out)))

        if int(change_str(out)) >1: _status='1'
        else:
            #启动目标MD服务
            out=exec_cli(Start_MD)
            if "Error" in out or '错误' in out: 
                _status='0'
            else: 
                _status="1"
        return {"status" : _status , "output": out }

#停止MD
class MDStopService(Resource):
    # @jwt_required()
    def get(self):
        out=exec_cli(Stop_MD)
        _out=exec_cli(_Stop_MD)
        
        if int(_out) ==1: 
            _status='1'
        else: 
            _status="0"
        
        return {"status" : _status}

#启动ME
class MEStartService(Resource):
    # @jwt_required()
    def get(self):
        #检查是否已经启动过
        out=exec_cli(PS_EF_ME)
        print(change_str(out))

        if int(change_str(out))>1: _status='1'
        else:
            out=exec_cli(Start_ME)
        
            if "Error" in out or '错误' in out: 
                _status='0'
            else: 
                _status="1"
        return {"status" : _status , "output": out }

#停止ME
class MEStopService(Resource):
    def get(self):
        out=exec_cli(Stop_ME)
        _out=exec_cli(_Stop_ME)
        
        if int(_out) ==1: 
            _status='1'
        else: 
            _status="0"
                
        return {"status" : _status}
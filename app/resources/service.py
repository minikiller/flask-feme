from flask_restful import Resource
from flask import request, jsonify, make_response
import json
from flask_jwt import jwt_required, current_identity
import os
import subprocess


#负责执行CLI命令,并返回结果
def exec_cli(_cmd):
    try:
        #os.system：获取程序执行命令的返回值。
        #os.popen： 获取程序执行命令的输出结果。
        val = os.popen(_cmd)
        out = val.read()  
    except:
        out = 'Error'

    return out


#列出服务
class ListService(Resource):
    # @jwt_required()
    def get(self):

        # MD服务检查
        mdout=exec_cli('ps -ef|grep ccme-mathcingengine-2.2.0-standalone.jar')
        if "ccme-mathcingengine-2.2.0-standalone.jar" in mdout :
           _mdStatus=1
        else:
           _mdStatus=0



        # ME服务检查
        meout=exec_cli('ps -ef |grep Me')
        if "ME" in meout :
           _meStatus=1
        else:
           _meStatus=0

        # 返回2个服务的真实状态   
        return jsonify({'md':_mdStatus,"ME":_meStatus})
        
# 

#启动MD
class MDStartService(Resource):
    # @jwt_required()
    def get(self):
        #out=exec_cli('ls -aslh .')
        out=exec_cli('java -cp ~/Project/9999-futures/ccme/matchingengine/target/ccme-mathcingengine-2.2.0-standalone.jar  quickfix.examples.ordermatch.MatchingEngine')
        if "Error" in out or '错误' in out: 
            _status='0'
        else: 
            _status="1"
        return {"status" : _status , "output": out }

#停止MD
class MDStopService(Resource):
    # @jwt_required()
    def get(self):
        out=exec_cli('ps -ef |grep JavaProgramName |awk '{print $2}'| grep -v grep |xargs kill -15')
        if "Error" in out or '错误' in out: 
            _status='0'
        else: 
            _status="1"
        _status = "on"
        return {"status" : _status}

#启动ME
class MEStartService(Resource):
    # @jwt_required()
    def get(self):
        #out=exec_cli('ls -aslh .')
        out=exec_cli('java -cp ~/Project/9999-futures/ccme/matchingengine/target/ccme-mathcingengine-2.2.0-standalone.jar  quickfix.examples.ordermatch.MatchingEngine')
        if "Error" in out or '错误' in out: 
            _status='0'
        else: 
            _status="1"
        return {"status" : _status , "output": out }

#停止ME
class MEStopService(Resource):
    def get(self):
        out=exec_cli('ps -ef |grep JavaProgramName |awk '{print $2}'| grep -v grep |xargs kill -15')
        if "Error" in out or '错误' in out: 
            _status='0'
        else: 
            _status="1"
        _status = "on"
        return {"status" : _status}
#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
File:   upload.py
Author: Lijiacai (v_lijiacai@baidu.com)
Date: 2019
Description:
"""

import os
import sys
import requests
import json

def upload(server,filename,task_id,user_id,task_log):
    url = "http://%s/fileupload/upload/upload"%server
    file_list = os.listdir("%s-splite"%filename)
    if not file_list:
        print "没有文件可以上传"
        return
    result = None
    for one in file_list:
        f = open("%s-splite/%s"%(filename,one), "r")
        files = {"file":(one,f)}
        data = {"user_id": user_id, "task_id": task_id, "filename": one, "task_log": task_log}
        response = requests.post(url=url, files=files, data=data)
        result = response.text
    if result:
        print result

if __name__ == '__main__':
    server=sys.argv[1]
    filename=sys.argv[2]
    #task_id=sys.argv[3]
    user_id=sys.argv[3]
    for data in sys.stdin:
        if not data:
	    continue
        try:
            task_id = json.loads(data).get("data").get("task_id")
            task_log = json.loads(data).get("data").get("task_log")
            upload(server,filename,task_id,user_id,task_log)
        except Exception as e:
            print str(e)
            pass

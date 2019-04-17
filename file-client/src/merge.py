#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
File:   .py
Author: Lijiacai (v_lijiacai@baidu.com)
Date: 2018-xx-xx
Description:
"""

import os
import sys
import requests
import json

def merge(server,filename,task_id,user_id,task_log):
    url = "http://%s/fileupload/upload/merge" % server
    data = {"user_id": user_id, "task_id": task_id, "filename":filename, "task_log": task_log}
    response = requests.post(url=url, data=data)
    print(response.text)
    print("Done!!!")
    

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
        except Exception as e:
            continue
        merge(server,filename,task_id,user_id,task_log)

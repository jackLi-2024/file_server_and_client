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
    url_del = "http://%s/fileupload/upload/delete_temp"%server
    file_list = os.listdir("%s-splite"%filename)
    if not file_list:
        raise Exception("No file to upload")
        return
    result = None
    isreturn = False
    error = ""
    for one in file_list:
        for i in range(3):
            try:
                f = open("%s-splite/%s"%(filename,one), "rb")
                files = {"file":(one,f)}
                data = {"user_id": user_id, "task_id": task_id, "filename": one, "task_log": task_log}
                response = requests.post(url=url, files=files, data=data)
                result = response.text
                break
            except Exception as e:
                error = str(e)
                isreturn = True
            try:
                f.close()
            except:
                pass
        if isreturn:
            data = {"user_id": user_id, "task_id": task_id}
            requests.post(url=url_del, data=data)
            raise Exception("upload defeat %s" % error)
    if result:
        print(result)

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
        upload(server,filename,task_id,user_id,task_log)

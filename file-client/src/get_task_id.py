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


def get_task_id(server,task_log,user_id):
    url = "http://%s/fileupload/upload/get_task_id" % server
    data = {"user_id": user_id, "task_log": task_log}
    response = requests.post(url=url, data=data)
    print(response.text)



if __name__ == '__main__':
    server=sys.argv[1]
    task_log=sys.argv[2]
    user_id=sys.argv[3]
    get_task_id(server,task_log,user_id)

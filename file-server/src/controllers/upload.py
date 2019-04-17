#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import logging
import signal
import ConfigParser
import time
from src.common import output
from src.common import util
from src import task

logger = logging.getLogger("upload")


class Upload(object):
    """"""

    def __init__(self):
        pass

    def upload_list(self, request):
        """upload"""
        return

    def get_task_id(self, request):
        """get task id"""
        user_id = request.form.get("user_id", None)
        task_log = request.form.get("task_log", None)
        os.system("mkdir -p ./data/%s/%s" % (user_id, task_log))
        task_id = str(time.time())
        os.system("mkdir -p ./temp/%s/%s" % (user_id, task_id))
        result = {"user_id": user_id, "task_id": task_id, "task_log": task_log}
        return output.normal_result(result)

    def upload(self, request):
        """upload file"""
        user_id = request.form.get("user_id", None)
        task_id = request.form.get("task_id", None)
        filename = request.form.get("filename", None)
        task_log = request.form.get("task_log", None)
        try:
            filestream = request.files["file"]
        except Exception as e:
            filestream = None
        if not all([user_id, task_id, filestream, filename]):
            return output.error_result(-1, (user_id, task_id, str(filestream), filename))
        try:
            os.listdir("./temp/%s/%s" % (user_id, task_id))
        except:
            return output.error_result(-1, u"Task_id Error")
        try:
            filestream.save("./temp/%s/%s/%s" % (user_id, task_id, filename))
        except:
            return output.error_result(-1, u"Shard_file upload Error-->[%s]" % filename)
        result = {"user_id": user_id, "task_id": task_id, "filename": filename,
                  "task_log": task_log}

        return output.normal_result(result)

    def merge(self, request):
        """merge"""
        user_id = request.form.get("user_id", None)
        task_id = request.form.get("task_id", None)
        filename = request.form.get("filename", None)
        task_log = request.form.get("task_log", None)
        if not all([user_id, task_id, filename]):
            os.system("rm -rf ./temp/%s/%s" % (user_id, task_id))
            return output.error_result(-1, u"Argument Error")
        try:
            os.listdir("./temp/%s/%s" % (user_id, task_id))
        except:
            os.system("rm -rf ./temp/%s/%s" % (user_id, task_id))
            return output.error_result(-1, u"Task_id Error")

        file_list = os.listdir("./temp/%s/%s" % (user_id, task_id))
        if file_list:
            rename_file = os.listdir("./data/%s/%s/" % (user_id, task_log))
            if filename in rename_file:
                now = time.time()
                os.system("mv ./data/%s/%s/%s ./data/%s/%s/%s_%s" % (
                    user_id, task_log, filename, user_id, task_log, filename, now))
            file_list.sort()
            for one in file_list:
                os.system("cat ./temp/%s/%s/%s >> ./data/%s/%s/%s" % (
                    user_id, task_id, one, user_id, task_log, filename))
        else:
            os.system("rm -rf ./temp/%s/%s" % (user_id, task_id))
            return output.error_result(-1, u"No file to merge")
        result = {"user_id": user_id, "task_id": task_id, "filename": filename,
                  "task_log": task_log}
        os.system("rm -rf ./temp/%s/%s" % (user_id, task_id))
        return output.normal_result(result)

    def delete_temp(self, request):
        """delete"""
        user_id = request.form.get("user_id", None)
        task_id = request.form.get("task_id", None)
        os.system("rm -rf ./temp/%s/%s" % (user_id, task_id))
        result = {"user_id": user_id, "task_id": task_id}
        return output.normal_result(result)



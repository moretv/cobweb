#-*-coding: utf-8 -*-

import time
import json
import thread
import os
import sys

sys.path.append(os.path.join(sys.path[0], "Modules"))

# Run task in a thread
class Tasks:
    def __init__(self, para, hostName, Logger):
        import Module
        import Utiles
        self._hostName = hostName
        self._taskFreq = para["taskFreq"] if "taskFreq" in para else 0
        self._indexFreq = para["indexFreq"] if "indexFreq" in para else 15
        self._Message = Utiles.Message(para["dictString"], Logger)
        self._Module = Module.Module(self._Message, para["indexUrl"], para["downloadUrl"], Logger)
        self._taskUrl = para["taskUrl"] if "taskUrl" in para else False
        self._resultUrl = para["resultUrl"] if "resultUrl" in para else False
        self._Logger = Logger

    def _getPara(self, mod_name):
        self._Logger.debug("Get para for %s" % mod_name)
        text = self._Message.httpget(self._taskUrl, {"Module":mod_name, "Host":self._hostName})
        data = json.loads(self._Message.deciphering(text))
        return data

    def _postResult(self, mod_name, result):
        self._Logger.debug("Post result for %s" % mod_name)
        text = self._Message.httpget(self._resultUrl, {"Module":mod_name, "Host":self._hostName, "Result":result}, False)
        res = json.loads(text)
        if 1 == res["status"]:
            self._Logger.debug("Post success %s" % mod_name)
        else:
            self._Logger.error("Post failed %s" % mod_name)
        return

    def _doTask(self, fname, mod_name):
        task_module = __import__(mod_name)
        self._Logger.info("Start thread %s" % fname)
        while True:
            try:
                self._Logger.info("Thread one task %s" % fname)
                if self._taskUrl:
                    data = self._getPara(mod_name)
                    result = task_module.task(data)
                else:
                    result = task_module.task()
                if self._resultUrl:
                    self._postResult(mod_name, result)
                if fname not in self._Module.module_status:
                    self._Logger.info("Thread expired %s" % fname)
                    break
                if "reload" == self._Module.module_status[fname]:
                    self._Logger.info("Thread module reload %s" % fname)
                    reload(task_module)
                    self._Module.module_status[fname] = "keep"
            except:
                pass
            finally:
                time.sleep(self._taskFreq)
        self._Logger.info("Terminal thread %s" % fname)
        thread.exit()

    def start(self):
        try:
            while True:
                try:
                    fnames = self._Module.check()
                    for fname in fnames:
                        self._Logger.info("New module find %s" % fname)
                        if ".py" != fname[-3:] : continue
                        if "lib_" == fname[0:4] : continue
                        self._Logger.debug("Ready to start module %s" % fname)
                        thread.start_new_thread(self._doTask, (fname, fname[0:-3]))
                except:
                    self._Logger.error("Thread create error")
                    pass
                finally:
                    time.sleep(self._indexFreq)
        except (IOError,EOFError,KeyboardInterrupt):
            print "...Process stop..."
            return

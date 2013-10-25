#!/usr/bin/env python
#-*-coding: utf-8 -*-

import random
import Cobweb.Modules

freq = 3
dictString = "ThankYouForChoosingMoreTV"
indexUrl = "http://127.0.0.1:8080/cobweb/index"
downloadUrl = "http://127.0.0.1:8080/cobweb/download/"

Tasks = Cobweb.Modules.Tasks(freq, dictString, indexUrl, downloadUrl)

def para(mod_name):
    if mod_name == "sample_mod":
        res = random.randint(1,10)
    else:
        res = False
    return res

def callback(result):
    print "Result:", result

Tasks.start(para, callback)
# Tasks.start(False, False)

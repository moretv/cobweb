#!/usr/bin/env python
#-*-coding: utf-8 -*-

import random
import Cobweb.Modules

freq = 3
dictString = "ThankYouForChoosingMoreTV"
indexUrl = "http://127.0.0.1:8080/cobweb/index"
downloadUrl = "http://127.0.0.1:8080/cobweb/download/"

Tasks = Cobweb.Modules.Tasks(freq, dictString, indexUrl, downloadUrl)

nums = [1, 2, 3, 4, 5]
count = 0

def para(mod_name):
    global nums
    global count
    print 123
    if mod_name == "sample_mod":
        if count >= len(nums): count = 0
        res = nums[count]
        count += 1
    else:
        res = False
    return res

def callback(result):
    print "Result:", result

Tasks.start(para, callback)
# Tasks.start(False, False)

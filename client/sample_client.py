#!/usr/bin/env python
#-*-coding: utf-8 -*-

import random
import Cobweb.Modules

freq = 3
dictString = "ThankYouForChoosingMoreTV"
indexUrl = "http://127.0.0.1:8080/cobweb/index"
downloadUrl = "http://127.0.0.1:8080/cobweb/download/"

Tasks_1 = Cobweb.Modules.Tasks(freq, dictString, indexUrl, downloadUrl)
def para(mod_name):
    n = random.randint(1,10)
    return n
Tasks_1.start(para)

# Tasks_2 = Cobweb.Modules.Tasks(freq, dictString, indexUrl, downloadUrl)
# Tasks_2.start()
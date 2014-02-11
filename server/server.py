#!/usr/bin/env python
#-*-coding: utf-8 -*-

import json
import web
import Cobweb.Fname
import Cobweb.Task

# dict_string for encryption
dictString = "ThankYouForChoosingMoreTV"

Fname = Cobweb.Fname.Fname(dictString)
Task = Cobweb.Task.Task()

urls = (
    '/cobweb/index', 'index', # Provide modules' list
    '/cobweb/download/(.+)', 'download', # Provide module files
    '/cobweb/parameter', 'parameter', # Provide task para
    '/cobweb/result', 'result', # Get task's result 
    '/cobweb/reindex', 'reindex',  # Rebuild the index (Manual)
)

class index:
    def GET(self):
        return Fname.index()  # Provide modules' list

class download:
    def GET(self, fname):
        return Fname.files(fname) # Provide module files

class parameter:
    def POST(self):
        data = web.input()
        Host = data["Host"] if "Host" in data else "unknow"
        Module = data["Module"] if "Module" in data else False
        ### not ready ###
        task = Task.request(Module, Host)
        #################
        para = Fname.encryption(json.dumps(task))
        return para

class result:
    def POST(self):
        data = web.input()
        Host = data["Host"] if "Host" in data else "unknow"
        Module = data["Module"] if "Module" in data else False
        Result = data["Result"] if "Result" in data else False
        ### not ready ###
        status = Task.response(Module, Host, Result)
        #################
        return status
        
class reindex:
    def GET(self):
        return Fname.newindex() # Rebuild the index
        
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

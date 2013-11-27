#!/usr/bin/env python
#-*-coding: utf-8 -*-

import json
import web
import Cobweb.Fname
import Cobweb.Task

Fname = Cobweb.Fname.Fname("ThankYouForChoosingMoreTV")
Task = Cobweb.Task.Task()

urls = (
    '/cobweb/index', 'index',
    '/cobweb/download/(.+)', 'download',
    '/cobweb/reindex', 'reindex',  # When Modules have been changed, rebuild the index
    '/cobweb/list', 'list',
    '/cobweb/result', 'upload',
)

class index:
    def GET(self):
        return Fname.index()  # Get modules' index

class download:
    def GET(self, fname):
        return Fname.files(fname) # Get module file's text

class reindex:
    def GET(self):
        return Fname.newindex() # Rebuild modules' index

class list:
    def POST(self):
        data = web.input()
        Host = data["Host"] if "Host" in data else "unknow"
        Module = data["Module"] if "Module" in data else False
        task = Task.request(Module, Host)
        return Fname.encryption(json.dumps(task))

class upload:
    def POST(self):
        data = web.input()
        Host = data["Host"] if "Host" in data else "unknow"
        Module = data["Module"] if "Module" in data else False
        Result = data["Result"] if "Result" in data else False
        return Task.response(Module, Host, Result)        

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

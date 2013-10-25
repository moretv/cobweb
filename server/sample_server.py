#!/usr/bin/env python
#-*-coding: utf-8 -*-

import json
import web
import Cobweb.Fname

Fname = Cobweb.Fname.Fname("ThankYouForChoosingMoreTV")

urls = (
    '/cobweb/index', 'index',
    '/cobweb/download/(.+)', 'download',
    '/cobweb/reindex', 'reindex',  # When Modules have been changed, rebuild the index
    '/cobweb/list', 'list',
)

class index:
    def GET(self):
        return Fname.index()  # Get modules' index

class download:
    def GET(self, fname):
        try:
            result = Fname.files(fname) # Get module file's text
        except:
            result = ""
        finally:
            return result

class reindex:
    def GET(self):
        return Fname.newindex() # Rebuild modules' index

class list:
    def GET(self):
        task_list = [
            "red",
            "blue",
            "yellow",
            "orange"
        ]
        return Fname.encryption(json.dumps(task_list))

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
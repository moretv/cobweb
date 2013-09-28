#!/usr/bin/env python
#-*-coding: utf-8 -*-

import web
import Cobweb.Fname

Fname = Cobweb.Fname.Fname("ThankYouForChoosingMoreTV")

urls = (
    '/cobweb/index', 'index',
    '/cobweb/download/(.+)', 'download',
    '/cobweb/reindex', 'reindex'  # When Modules have been changed, rebuild the index
)

class index:
    def GET(self):
        return Fname.index()

class download:
    def GET(self, fname):
        try:
            result = Fname.files(fname)
        except:
            result = ""
        finally:
            return result

class reindex:
    def GET(self):
        return Fname.newindex()

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
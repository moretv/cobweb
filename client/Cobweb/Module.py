#-*-coding: utf-8 -*-

import json
import os
import sys

# Get modules' info from remote server
class Module:
    def __init__(self, Message, index_url, download_url, Logger):    
        self._index_url = index_url
        self._download_url = download_url
        self._root_path = os.path.join(sys.path[0], "Modules")
        self._file = {}
        self.module_status = {}
        self._Message = Message
        self._Logger = Logger

    def _update(self, filename, md5sum):
        try:
            text = self._Message.httpget(self._download_url+'/'+filename)
            data = self._Message.deciphering(text)
            new_md5sum = self._Message.md5sum(data)
            self._Logger.info("MD5: %s %s" % (filename, new_md5sum))
            if md5sum == new_md5sum:
                filepath = os.path.join(self._root_path, filename)
                f = open(filepath, 'w')
                f.write(data)
                f.close()
                self._Logger.info("Update success %s" % filename)
                return True
            else:
                self._Logger.error("Update not match %s" % filename)
                return False
        except:
            self._Logger.error("Update failed %s" % filename)
            return False

    def check(self):
        try:
            self._Logger.info("Check modules %s" % self._index_url)
            text = self._Message.httpget(self._index_url)
            data = json.loads(self._Message.deciphering(text))
            items = {}
            status = {}
            new = []
            for i in data:
                self._Logger.debug("Index filename %s" % i["filename"])
                if i["filename"] in self._file:
                    items[i["filename"]] = self._file[i["filename"]]
                    status[i["filename"]] = self.module_status[i["filename"]]
                    if i["timestamp"] > self._file[i["filename"]]["timestamp"]:
                        update = self._update(i["filename"], i["md5sum"])
                        if update: 
                            items[i["filename"]] = {"md5sum":i["md5sum"], "timestamp": i["timestamp"]}
                            status[i["filename"]] = "reload"
                else:
                    update = self._update(i["filename"], i["md5sum"]) 
                    if update: 
                        items[i["filename"]] = {"md5sum":i["md5sum"], "timestamp": i["timestamp"]}
                        new.append(i["filename"])
                        status[i["filename"]] = "keep"
            self._file = items
            self.module_status = status
            self._Logger.info("Check modules success %s" % self._index_url)
            return new
        except:
            self._Logger.error("Check failed %s" % self._index_url)
            return False
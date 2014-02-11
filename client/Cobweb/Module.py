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
        self._file = {} # Modules' list
        self.module_status = {} # Modules' status
        self._Message = Message
        self._Logger = Logger

    # Download file
    def _update(self, path, filename, md5sum):
        try:
            fname = os.path.join(path, filename)
            text = self._Message.httpget(self._download_url+'/'+fname)
            data = self._Message.deciphering(text)
            new_md5sum = self._Message.md5sum(data)
            self._Logger.info("MD5: %s %s" % (fname, new_md5sum))
            if md5sum == new_md5sum:
                dirpath = os.path.join(self._root_path, path)
                if not os.path.isdir(dirpath): os.makedirs(dirpath)
                filepath = os.path.join(self._root_path, fname)
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

    # Check the files' info and status
    def check(self):
        try:
            self._Logger.info("Check modules %s" % self._index_url)
            # Get modules' list
            text = self._Message.httpget(self._index_url)
            data = json.loads(self._Message.deciphering(text))
            
            items = {}
            status = {}
            new = []
            for i in data:
                fname = os.path.join(i["path"], i["filename"])
                self._Logger.debug("Index filename %s" % fname)
                if fname in self._file: # the File is old
                    self._Logger.debug("Find a old file %s" % fname)
                    # initialize Module's info and status
                    items[fname] = self._file[fname]
                    status[fname] = self.module_status[fname]
                    
                    if i["timestamp"] > self._file[fname]["timestamp"]: # the File has been updated
                        update = self._update(i["path"], i["filename"], i["md5sum"]) # Download the new file
                        if update: 
                            items[fname] = {"md5sum":i["md5sum"], "timestamp": i["timestamp"]}
                            # Check file's name
                            if ('' == i["path"]) and ("lib_" != i["filename"][0:4]) and (".py" == fname[-3:]):
                                # the file is a available Cobweb module
                                status[fname] = "reload"
                            else:
                                status[fname] = "block"
                                
                else: # find a new File
                    self._Logger.debug("Find a new file %s" % fname)
                    update = self._update(i["path"], i["filename"], i["md5sum"]) # Download the new file
                    if update: 
                        items[fname] = {"md5sum":i["md5sum"], "timestamp": i["timestamp"]}
                        # Check file's name
                        if ('' == i["path"]) and ("lib_" != i["filename"][0:4]) and (".py" == fname[-3:]):
                            # the file is a available Cobweb module
                            new.append(fname) # need start a new thread
                            status[fname] = "keep"
                        else:
                            status[fname] = "block"
            
            # rebuild the Modules' info and status
            self._file = items
            self.module_status = status
            self._Logger.info("Check modules success %s" % self._index_url)
            return new
        except:
            self._Logger.error("Check failed %s" % self._index_url)
            return False
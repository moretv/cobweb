#-*-coding: utf-8 -*-

import time
import thread
import hashlib
import urllib2
import json
import os
import sys

sys.path.append(os.path.join(sys.path[0], "Modules"))

# Run task in a thread
class Tasks:
    def __init__(self, freq, dict_string, index_url, download_url):
        self._freq = freq
        self._Modules = Modules(dict_string, index_url, download_url)

    def do_task(self, mod_name, fname, para):
        task_module = __import__(mod_name)
        print "Start: %s" % fname
        while True:
            try:
                if para:
                    task_module.task(para(mod_name))
                else:
                    task_module.task()
                if fname not in self._Modules.module_status: break 
                if "reload" == self._Modules.module_status[fname]:
                    print "Reload: %s" % fname
                    reload(task_module)
                    self._Modules.module_status[fname] = "keep"
            except:
                pass
            finally:
                time.sleep(self._freq)
        print "End: %s" % fname
        thread.exit()

    def start(self, para=False):
        while True:
            try:
                fnames = self._Modules.check()
                for fname in fnames:
                    if ".py" != fname[-3:] : continue
                    mod_name = fname[0:-3]
                    thread.start_new_thread(self.do_task, (mod_name, fname, para))
            except:
                pass
            finally:
                time.sleep(15)

# Get modules' info from remote server
class Modules:
    def __init__(self, dict_string, index_url, download_url):
        self._dict_string_length = len(dict_string)
        dict_number = []
        for char in dict_string: dict_number.append(ord(char)-31) 
        self._dict_num = dict_number       
        self._index_url = index_url
        self._download_url = download_url
        self._root_path = os.path.join(sys.path[0], "Modules")
        self._file = {}
        self.module_status = {}

    def _md5sum(self, text):
        m = hashlib.md5()
        m.update(text)
        return m.hexdigest()

    def _deciphering(self, text):
        try:
            count = 0
            result = ""
            for char in text:
                new_number = ord(char)
                if new_number >= 32 and new_number <= 126:
                    nn = new_number - self._dict_num[count]
                    if nn < 32: nn = nn + 126 - 31
                    new_char = chr(nn)
                else:
                    new_char = char
                result += new_char
                count += 1
                if count == self._dict_string_length: count = 0
            return result
        except:
            return False

    def _httpget(self, url):
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request).read()
            return response
        except:
            return False

    def _update(self, filename, md5sum):
        try:
            text = self._httpget(self._download_url+filename)
            data = self._deciphering(text)
            new_md5sum = self._md5sum(data)
            if md5sum == new_md5sum:
                filepath = os.path.join(self._root_path, filename)
                f = open(filepath, 'w')
                f.write(data)
                f.close()
                return True
            else:
                return False
        except:
            return False

    def check(self):
        try:
            text = self._httpget(self._index_url)
            data = json.loads(self._deciphering(text))
            items = {}
            status = {}
            new = []
            for i in data:
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
            return new
        except:
            return False
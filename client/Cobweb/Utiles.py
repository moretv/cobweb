#-*-coding: utf-8 -*-

import hashlib
import urllib
import urllib2
import os
import sys

# Some tools

# RPC method
class Message:
    def __init__(self, dict_string, Logger):
        # dict_string for encryption
        self._dict_string_length = len(dict_string)
        dict_number = []
        for char in dict_string: dict_number.append(ord(char)-31)
        self._dict_num = dict_number
        
        self._Logger = Logger # Logger

    def deciphering(self, text):
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
            self._Logger.info("Deciphering success")
            return result
        except:
            self._Logger.error("Deciphering failed")
            return False

    def md5sum(self, text):
        m = hashlib.md5()
        m.update(text)
        return m.hexdigest()

    def httpget(self, url, post_data=False, decipher=True):
        try:
            if post_data: # post method
                self._Logger.info("POST %s" % url)
                data = urllib.urlencode(post_data)
                request = urllib2.Request(url, data)
            else: # get method
                self._Logger.info("GET %s" % url)
                request = urllib2.Request(url)
            response = urllib2.urlopen(request).read()
            self._Logger.info("HTTP Success %s" % url)
            return response
        except:
            self._Logger.error("HTTP Failed %s" % url)
            return False

# Logger...
class Logger:
    def __init__(self, filename="cobweb.log", level=0):
        import logging
        self._print = False
        self._logger = logging.getLogger()
        hdlr = logging.FileHandler(os.path.join(sys.path[0], filename))
        formatter = logging.Formatter('%(asctime)s %(message)s')
        hdlr.setFormatter(formatter)
        self._logger.addHandler(hdlr)
        if 1 == level:
            self._logger.setLevel(logging.DEBUG)
        elif 2 == level:
            self._logger.setLevel(logging.INFO)
        elif 3 == level:
            self._logger.setLevel(logging.WARNING)
        elif 4 == level:
            self._logger.setLevel(logging.ERROR)
        elif 5 == level:
            self._logger.setLevel(logging.CRITICAL)
        else:
            self._print = True

    def debug(self, text):
        self._logout(text, 1)
        return

    def info(self, text):
        self._logout(text, 2)
        return

    def warning(self, text):
        self._logout(text, 3)
        return

    def error(self, text):
        self._logout(text, 4)
        return

    def critical(self, text):
        self._logout(text, 5)
        return

    def _logout(self, text, level):
        if self._print:
            print text
        elif 1 == level:
            self._logger.debug(text)
        elif 2 == level:
            self._logger.info(text)
        elif 3 == level:
            self._logger.warning(text)
        elif 4 == level:
            self._logger.error(text)
        elif 5 == level:
            self._logger.critical(text)
        return

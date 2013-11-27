#-*-coding: utf-8 -*-

class Task:
    def __init__(self):
        return

    def request(self, Module, Host):
        return "http://www.moretv.com.cn"

    def response(self, Module, Host, Result):
        print Result
        res = '{"status":1}'
        return res
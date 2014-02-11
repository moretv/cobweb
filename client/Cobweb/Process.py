#-*-coding: utf-8 -*-

from signal import SIGINT,SIGTERM,SIGKILL
import time
import os
import sys

class Daemon:
    def __init__(self, filename, Logger):
        self._Logger = Logger
        self._pidFile = os.path.join(sys.path[0], filename)
        self.killAll()

    # killall process
    def killAll(self):
        try:
            pf  = file(self._pidFile,'r')
            for pid in pf.readlines():
                self._kill(pid)
            pf.close()
            os.remove(self._pidFile)
        except:
            pass
    
    # kill a process
    def _kill(self, pid):
        try:
            pidno = int(pid.strip())
            #print "killing PROCESS... %s" % pidno
            os.kill(pidno,SIGINT)
            time.sleep(2)
            os.kill(pidno,SIGTERM)
            time.sleep(2)
            os.kill(pidno,SIGKILL)
        except:
            pass

    # make a new process
    def start(self, Task):
        pid = os.fork()
        if 0 == pid:
            pidno = os.getpid()
            file(self._pidFile,'a').write("%s\n" % pidno)
            print "starting PROCESS... %s" % pidno
            Task.start()


        

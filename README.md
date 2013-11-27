cobweb
======
a distributed task execution system

* easy to dispatch task script and autoreload
* multi-process task model
* multi-thread task running
* support task parameter router



        pidFile = "cobweb.pid"
        hostName = "TestHost"
        logFile = "cobweb.log"
        logLevel = 1 # if logLevel > 0 then run as a daemon

        taskList = [
            {
                "dictString" : "ThankYouForChoosingMoreTV",
                "indexUrl" : "http://127.0.0.1:8080/cobweb/index",
                "downloadUrl" : "http://127.0.0.1:8080/cobweb/download",
                "taskFreq" : 5, # Option
                "indexFreq" : 15, # Option        
                "taskUrl" : "http://127.0.0.1:8080/cobweb/list",  # Option
                "resultUrl" : "http://127.0.0.1:8080/cobweb/result", # Option
            }
        ]

        import Cobweb.Process
        import Cobweb.Thread
        import Cobweb.Utiles

        Logger = Cobweb.Utiles.Logger(logFile, logLevel)
        Daemon = Cobweb.Process.Daemon(pidFile, Logger)

        try:
            for task in taskList:
                Daemon.start(Cobweb.Thread.Tasks(task, hostName, Logger))
            if 0 == logLevel:
                import time
                while True: time.sleep(9999)
        except (IOError,EOFError,KeyboardInterrupt):
            Daemon.killAll()
            exit(0)

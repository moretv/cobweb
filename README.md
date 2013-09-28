cobweb
======
a distributed task execution system

* easy to dispatch task script and autoreload
* multi-thread task running
* support task parameter router



		import Cobweb.Modules
		
		freq = 3
		dictString = "ThankYouForChoosingMoreTV"
		indexUrl = "http://127.0.0.1:8080/cobweb/index"
		downloadUrl = "http://127.0.0.1:8080/cobweb/download/"
		
		Tasks = Cobweb.Modules.Tasks(freq, dictString, indexUrl, downloadUrl)
		Tasks.start()

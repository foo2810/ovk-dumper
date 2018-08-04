# File Operation Utilities

import threading
import queue
import time
from pathlib import Path

class SaveBufferFull(Exception):
	def __init__(self):
		pass


class SaveBinThread(threading.Thread):
	__QUEUESIZE = 1000

	def __init__(self):
		super().__init__()
		self.exitFlg = False
		self.que = queue.Queue(SaveBinThread.__QUEUESIZE)
	
	def run(self):
		while (not self.exitFlg):
			if (not self.que.empty()):
				item = self.que.get()
				self.__saveFile(item[0], item[1])
			else:
				time.sleep(0.01)
		
		while (not self.que.empty()):
			item = self.que.get()
			self.__saveFile(item[0], item[1])
		
		#print("SaveFileThread exiting")
	
	def quit(self):
		self.exitFlg = True
	
	def saveRequest(self, data, file):
		item = (data, file)
		try:
			self.que.put(item)
		except queue.Full:
			raise SaveBufferFull
	
	def __saveFile(self, data, path):
		if isinstance(path, str):
			st = open(path, "wb")
		elif isinstance(path, Path):
			st = path.open("wb")
		else:
			raise TypeError
			
		st.write(data)
		st.flush()
		st.close()


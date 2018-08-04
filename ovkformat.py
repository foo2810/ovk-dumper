# OVK FILE FORMAT
# USED BY SUMMER POCKETS

import sys
from pathlib import Path
from fileUtil import *
from binaryUtil import *


class NotUnderstandError(Exception):
	def __init__(self, obj):
		self.type = type(obj)
	
	
class OVKFormat(BinaryReader):
	def __init__(self, bData):
		super().__init__(bData, 0)
		self.i = 0	# For iteration
		
		self.oggList = list()
		
		self.numOggFile = byteToIntLE(super().readBytes(4))
		
		oggFileSize = byteToIntLE(super().readBytes(4))
		oggFileHead = byteToIntLE(super().readBytes(4))
		content2 = byteToIntLE(super().readBytes(4))
		self.oggList.append((self.numOggFile, oggFileSize, oggFileHead, content2))
		
		headerEnd = oggFileHead - 1
		if headerEnd < 0:
			sys.stderr.write("I understand wrong ovk format...")
			logging.critical("I understand wrong ovk format")
			raise NotUnderstandError
		
		for i in range(self.numOggFile):
			content1 = byteToIntLE(super().readBytes(4))
			oggFileSize = byteToIntLE(super().readBytes(4))
			oggFileHead = byteToIntLE(super().readBytes(4))
			content2 = byteToIntLE(super().readBytes(4))
			self.oggList.append((content1, oggFileSize, oggFileHead, content2))
		
		#self.pos_debug = super().getCurrentPosition() - 17
	
	def __iter__(self):
		return self
	
	def __next__(self):
		if self.i == self.numOggFile:
			self.i = 0
			raise StopIteration
		
		item = self.oggList[self.i]
		self.i += 1
		
		return item
	
	def extractOggRawData(self, meta):
		save = super().getCurrentPosition()
		super().moveTo(meta[2])
		data = super().readBytes(meta[1])
		super().moveTo(save)
		return data
	
	def printHeaders(self):
		for ogg in self.oggList:
			print("Content1   :\t" + hex(ogg[0]) + "(" + str(ogg[0]) + ")")
			print("OggFileSize:\t" + hex(ogg[1]))
			print("OggFileHead:\t" + hex(ogg[2]))
			print("Content2   :\t" + hex(ogg[3]) + "(" + str(ogg[3]) + ")")
			print("---")
		
		#print("Header End pos: ", hex(self.pos_debug))
		print("Number of ogg data: ", len(self.oggList) - 1)

def usage():
	sys.stderr.write("Usage: py readovk.py <file> [<save_dir> <option>]\n")
	sys.stderr.write("[Caution]\n")
	sys.stderr.write("Default save directory is current directory\n\n")
	sys.stderr.write("[Option]\n")
	sys.stderr.write("-r: Show ovk headers\n")
	sys.stderr.write("-d: Dump ogg files\n")
	sys.stderr.write("-a: Do everything\n")


# For debug ?
def main():
	import logging
	logging.basicConfig(format="[%(asctime)s] %(levelname)s:%(message)s", filename="log.txt", level=logging.DEBUG)

	argv = sys.argv
	argc = len(argv)
	option = ""
	pathes = list()
	
	if argc < 2:
		usage()
		logging.info("Too few arguments")
		sys.exit(1)
	else:
		for arg in argv[1:]:
			if len(arg) > 1 and arg[0] == "-":
				option = option + arg[1:]
			else:
				pathes.append(arg)
	if len(option) == 0:
		option = "r"
	
	ovkFile = None
	saveDir = None
	if len(pathes) < 1:
		usage()
		logging.info("Too few pathes")
		sys.exit(1)
	elif  len(pathes) == 1:
		ovkFile = Path(pathes[0])
		saveDir = "./"
	else:
		ovkFile = Path(pathes[0])
		saveDir = pathes[1]
	
	if not ovkFile.exists():
		sys.stderr.write("File not found")
		logging.info("File not found - ", ovkFile)
		sys.exit(1)
		
	print(option)
	
	st = ovkFile.open("rb")
	data = st.read()
	st.close()
	
	ovk = OVKFormat(data)
	
	if "r" in option or "a" in option:
		print("Headers:")
		ovk.printHeaders()
	
	if "d" in option or "a" in option:
		saveHandler = SaveBinThread()
		saveHandler.start()
		
		cnt = 0
		for meta in ovk:
			cnt += 1
			bdata = ovk.extractOggRawData(meta)
			path = Path(saveDir) / ovkFile.stem
			path.mkdir(parents=True, exist_ok=True)
			path = path / "{}_{}.ogg".format(ovkFile.stem, cnt)
			saveHandler.saveRequest(bdata, path)
		
		saveHandler.quit()
		#print("Finish")
	
	#ovk.printHeaders()


if __name__ == "__main__":
	main()

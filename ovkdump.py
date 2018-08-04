# ovkdump

import sys
from ovk.ovkformat import *
from utils.fileUtil import *

class InvalidArgument(Exception):
	def __init__(self, arg, idx, description=""):
		self.arg = arg
		self.index = idx
		self.description = description
		
	def getTargetArg(self):
		return self.arg
	
	def getDescription(self):
		return self.description

def usage():
	sys.stderr.write("Usage: py readovk.py -s <save_dir> [-f <file> -d <directory>]\n")
	

def main():
	import logging
	logging.basicConfig(format="[%(asctime)s] %(levelname)s:%(message)s", filename="log_ovkdump.txt", level=logging.DEBUG)
	
	logging.info("Start ovkdump")
	
	argv = sys.argv
	argc = len(argv)
	
	# arguments parse
	# インデント深すぎぃ
	option = ""
	fileList = list()
	dirList = list()
	saveDir = None
	cnt = 1
	try:
		while cnt < argc:
			arg = argv[cnt]
			if arg[0] == "-" and len(arg) > 1:
				if len(arg) != 2:
					raise InvalidArgument(arg, cnt)
					
				if arg[1] == "f":
					cnt += 1
					while cnt < argc:
						arg = argv[cnt]
						# if arg is option
						if arg[0] == "-":
							cnt -= 1
							break
						
						fileList.append(arg)
						
						cnt += 1
						
				elif arg[1] == "d":
					cnt += 1
					while cnt < argc:
						arg = argv[cnt]
						# if arg is option
						if arg[0] == "-":
							cnt -= 1
							break
						
						dirList.append(arg)
						
						cnt += 1
						
				elif arg[1] == "s":
					cnt += 1
					while cnt < argc:
						arg = argv[cnt]
						# if arg is option
						if arg[0] == "-":
							cnt -= 1
							break
						
						if saveDir is not None:
							raise InvalidArgument(arg, cnt, "Duplicate save directory")
						else:
							saveDir = arg
						
						cnt += 1
						
				else:
					raise InvalidArgument(arg, cnt)
					
			else:
				raise InvalidArgument(arg, cnt)
			
			cnt += 1
			
	except InvalidArgument as e:
		usage()
		sys.stderr.write("\n")
		sys.stderr.write("InvalidArgument: " + e.getTargetArg())
		sys.stderr.write("\n")
		sys.stderr.write("Description: " + e.getDescription())
		sys.stderr.write("\n")
		sys.exit(1)
	
	except Exception as e:
		logging.info("Raise Unknown error in parsing arguments")
		logging.info("ovkdump exiting")
		sys.stderr.write("Raise Unknown error")
		print(e)
		
	
	if len(fileList) == 0 and len(dirList) == 0:
		logging.info("ovkdump exiting")
		usage()
		sys.exit(1)
	
	if saveDir is None:
		logging.info("ovkdump exiting")
		usage()
		sys.stderr.write("Save directory is not selected")
		sys.exit(1)
	
	
	
	
	print("Files:")
	print(fileList)
	print("Directories:")
	print(dirList)
	
	allFileList = list()
	
	for file in fileList:
		path = Path(file)
		if not path.exists():
			logging.info("FileNotExist - {}".format(path))
			continue
			
		allFileList.append(path)
	
	for dir in dirList:
		dirPath = Path(dir)
		if not dirPath.is_dir():
			logging.info("NotDirectory or NotExist - {}".format(dirPath))
			continue
		
		fList = dirPath.glob("*.ovk")
		allFileList.extend(fList)
		
	print("All Files:")
	print(allFileList)
	
	savePathBase = Path(saveDir)
	if not savePathBase.is_dir():
		logging.info("NotDirectory or NotExist - {}".format(savePathBase))
		sys.stderr.write("Save directory is not found")
		logging.info("ovkdump exiting")
		sys.exit(1)
		
	saveHandler = SaveBinThread()
	saveHandler.start()
	logging.info("File save thread start")
	
	for file in allFileList:
		bdata = file.read_bytes()
		ovk = OVKFormat(bdata)
		save = savePathBase / file.stem
		#print("SavePathBase: ", savePathBase)
		
		save.mkdir(parents=True, exist_ok=True)
		
		i = 0
		for meta in ovk:
			i += 1
			oggRawData = ovk.extractOggRawData(meta)
			savePath = save / "{}_{}.ogg".format(file.stem, i)
			print("Dump to ", savePath)
			
			try:
				saveHandler.saveRequest(oggRawData, savePath)
			except SaveBufferFull as e:
				logging.warning("Save buffer is full")
				logging.info("ovkdump exiting")
				sys.stderr.write("Save buffer is full")
				saveHandler.quit()
				sys.exit(1)
			
			except Exception as e:
				logging.warning("Raise unknown error in save thread")
				logging.info("ovkdump exiting")
				sys.stderr.write(e)
				saveHandler.quit()
				sys.exit(1)
	
	saveHandler.quit()
	logging.info("File save thread exit")
	
	logging.info("ovkdump exiting")


if __name__ == "__main__":
	main()

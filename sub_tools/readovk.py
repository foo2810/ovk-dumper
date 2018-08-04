# read ovk


import sys
from pathlib import *
sys.path.append(str(Path.cwd().resolve()) + "../")

from ovk.ovkformat import *


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
	sys.stderr.write("Usage: python3 readovk.py -s <save_dir> [-f <file> -d <directory>]\n")
	

def main():
	import logging
	logging.basicConfig(format="[%(asctime)s] %(levelname)s:%(message)s", filename="log_readovk.txt", level=logging.DEBUG)
	
	logging.info("Start readovk")
	
	argv = sys.argv
	argc = len(argv)
	
	# arguments parse
	# インデント深すぎぃ
	option = ""
	fileList = list()
	dirList = list()
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
		logging.info("readovk exiting")
		sys.stderr.write("Raise Unknown error")
		print(e)
		
	
	if len(fileList) == 0 and len(dirList) == 0:
		logging.info("readovk exiting")
		usage()
		sys.exit(1)
	
	
	# For debug	
	#print("Files:")
	#print(fileList)
	#print("Directories:")
	#print(dirList)
	
	allFileList = list()
	
	for file_ in fileList:
		path = Path(file_)
		if not path.exists():
			logging.info("FileNotExist - {}".format(path))
			continue
			
		allFileList.append(path)
	
	for dir_ in dirList:
		dirPath = Path(dir_)
		if not dirPath.is_dir():
			logging.info("NotDirectory or NotExist - {}".format(dirPath))
			continue
		
		fList = dirPath.glob("*.ovk")
		allFileList.extend(fList)
		
	print("All Files:")
	print(allFileList)
	
	for file_ in allFileList:
		bdata = file_.read_bytes()
		ovk = OVKFormat(bdata)

		print("{}:".format(file_))
		ovk.printContents()
		print("******************************\n\n")
			
	
	logging.info("readovk exiting")


if __name__ == "__main__":
	main()

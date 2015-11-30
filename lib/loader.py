import os
import rpy2.robjects as robjects
from rpy2.robjects.packages import STAP

class AutoLoadRLibs:
	r = None

	def __init__(self, r_path):
		self.r = robjects.r
		for subdir, dirs, files in os.walk(r_path):
			for file in files:
				with open(os.path.join(subdir, file), 'r') as f:
					string = f.read()

				cust_namespace = subdir.replace(r_path, '')
				self.__dict__[cust_namespace] = STAP(string, cust_namespace)
	
	def __getattr__(self, key):
		return self.__dict__[key]

'''
Run all submodules as __main__ and execute their test procedure
 
Note there is a bug in pkgutil.walk_packages
excluding all modules that have the same name as modules in 
the standard library, see
http://bugs.python.org/issue14787
'''
if __name__ == '__main__':
	from fancytools.pystructure.runAllInDir import runAllInDir
	import os
	import __main__

	thisModName = os.path.splitext(os.path.basename(__main__.__file__))[0]


	runAllInDir(os.path.abspath(os.curdir), 
			exclude=[thisModName])
	

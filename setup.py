'''
usage:
 (sudo) python setup.py +
	 install		... local
	 register		... at http://pypi.python.org/pypi
	 sdist			... create *.tar to be uploaded to pyPI
	 sdist upload	... build the package and upload in to pyPI
'''

#########################
import fancywidgets as package
#########################


from setuptools import setup, find_packages
import os
import sys

def read(*paths):
	"""Build a file path from *paths* and return the contents."""
	try:
		f_name = os.path.join(*paths)
		with open(f_name, 'r') as f:
			return f.read()
	except IOError:
		print('%s not existing ... skipping' %f_name)
		return ''

setup(
	name			= package.__name__,
	version 		= package.__version__,
	author			= package.__author__,
	author_email	= package.__email__,
	url				= package.__url__,
	license			= package.__license__,
	install_requires= package.__depencies__,
	classifiers		= package.__classifiers__,
	description		= package.__doc__,
	packages		= find_packages(exclude=['tests*']),
	include_package_data=True,
	scripts			= [] if not os.path.exists('bin') else [
						os.path.join('bin',x) for x in os.listdir('bin')],
	long_description=(
		read('README.rst') + '\n\n' +
		read('CHANGES.rst') + '\n\n' +
		read('AUTHORS.rst')
		),
	)



#LAUNCHER NEEDS SOME WORK - UNTIL THATS DONE: DONT RUN THE FOLLOWING
INSTALL_QDESIGNER_STARTER = False
	
if INSTALL_QDESIGNER_STARTER:

	if 'install' in sys.argv:
		while True:
			answer = raw_input('Do you want to a start menu entry for the QDesigner with included fancyWidgets plugins? [Y,N] ')
			if answer.lower() in ('y', 'n', ''):
				break
			print("Please answer with 'Y' or 'N'")
		if answer == 'Y':
	
			from fancytools.os import PathStr, StartMenuEntry
			
			prog_path = PathStr(sys.executable).dirname().join('Scripts','fwdesigner.pyw')
			print('create start menu entry for Fw_QtDesigner located in %s' %prog_path)
			
			StartMenuEntry('Fw_QtDesigner', prog_path).create()

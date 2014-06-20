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

#import sys


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

#TODO: run as a seperate setup() with designerpath as destination
#TODO: OR append to designerpath for individual qtdesigner-starter
#import PyQt4.uic
import sys
from fancytools.os import PathStr, StartMenuEntry
#designerpath = PyQt4.uic.widgetPluginPath[0]
#print("\ncopying qt-designer plugings the the qt-designer plugin path '%s'"
#	%designerpath)
#p = PathStr('fwQtDesigner_plugins')
#for f in p:
#	p.join(f).copy(designerpath)

prog_path = PathStr(sys.executable).dirname().join('Scripts','fwdesigner.pyw')
print('create start menu entry for Fw_QtDesigner located in %s' %prog_path)

StartMenuEntry('Fw_QtDesigner', prog_path).create()
#icon=None,directory=None,
#				version='-', description='', categories=''
#

## remove the build
## else old and notexistent files could come again in the installed pkg
#mainPath = os.path.abspath(os.path.dirname(__file__))
#bPath = os.path.join(mainPath,'build')
#if os.path.exists(bPath):
	#shutil.rmtree(bPath)

#
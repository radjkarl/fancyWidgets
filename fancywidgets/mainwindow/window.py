# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

#own
#import nIOp

#foreign
#import os

from QtRec import QtGui

from menubar import MenuBar
import appbase


class MainWindow(QtGui.QMainWindow):
	'''
	default class to build Qt-windows for nIOp
	including the nIOp-icon and fullscreen with F11
	'''
	def __init__(self, title=''):
		super(MainWindow, self).__init__()
		self.app = QtGui.QApplication.instance()
		if not isinstance(self.app, appbase.application.Application):
			print 'Error: QApp is no instance from appbase.Application'
			return

		self.app.session.sigPathChanged.connect(self.setTitle)

		self._window_title = title
		self.setMenuBar(MenuBar())
		self.setTitle()


	def setTitle(self, path=''):
		#if self.app:
		if self._window_title:
			if path:
				title = "(%s) || %s" %(self._window_title,path)
			else:
				title = self._window_title
		else:
			title = path
		##if path.endswith('.pyz'):
		#title += ' || %s'%path
		self.setWindowTitle(title)






if __name__ == '__main__':
	#TODO: TEST into docstring
	from appbase.application import Application
	import sys
	app = Application([])
	#from widgets.window import Window
	#app = Application('Hello World')
	win = MainWindow(title='Hello World')
	win.show()
	#app.start()
	sys.exit(app.exec_())
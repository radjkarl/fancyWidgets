# -*- coding: utf-8 -*-
from pyqtgraph_karl.dockarea import DockArea as pgDockArea
# from QtRec.QtGui import QWidget
# 
# b = list(pgDockArea.__bases__)
# for n,l in enumerate(b):
# 	if l.__name__ == 'QWidget':
# 		b[n] = QWidget
# pgDockArea.__bases__ = tuple(b)

class DockArea(pgDockArea):
	'''
	save the initial position of a dock and
	restores it if wished
	'''


	def addDock(self, dock, *args, **kwargs):
		dock.init_position = kwargs
		return super(DockArea,self).addDock(dock, *args, **kwargs)


	def restore(self):
		for dock in self.docks:
			dock.embedd()
			self.moveDock(dock, dock.init_position)


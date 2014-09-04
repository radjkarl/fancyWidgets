# -*- coding: utf-8 -*-
from pyqtgraph.dockarea.Dock import DockLabel as pgDockLabel
from pyqtgraph.dockarea.DockDrop import DockDrop as pgDockDrop

import pyqtgraph.dockarea as pgDock
#-> docks müssen beim speichern berücksichtigt werden
#-> doppelclick fährt docks ein

#from QtRec import QtGui, QtCore
from pyqtgraph.Qt import QtGui, QtCore

#pgDock.Dock.__bases__ = (QtGui.QWidget, pgDockDrop)
class Dock(pgDock.Dock):
	'''adding function: setWidget to normal Dock-class'''
	def __init__(self, name, area=None, size=(1,1), 
				widget=None, hideTitle=False, autoOrientation=False,
				closable=True, minimizable=True
				):
		super(Dock, self).__init__(name, area, size, widget, hideTitle, 
								autoOrientation, closable, minimizable)
		self._pparent = None
		self._saved_state = None
		
		self.label.menu = DockLabelMenu(self)
		


	def toggleFullscreen(self):
		if self.isFullScreen():
			self.embedd()
			self.showNormal()
			if self._saved_state:
				self.area.addDock(self)
				self.area.restoreState(self._saved_state)
				self._saved_state = None
		else:
			if self.area:
				self._saved_state = self.area.saveState()
			self.release()
			self.showFullScreen()




	#TODO: do i still need this method???
	def setWidget(self, widget, index=0, row=None, col=0, rowspan=1, colspan=1):
		"""
		Add a new widget to the interior of this Dock.
		Each Dock uses a QGridLayout to arrange widgets within.
		"""
		if row is None:
			row = self.currentRow
		self.currentRow = max(row+1, self.currentRow)
		if index > len(self.widgets)-1:
			#add new widget
			self.widgets.append(widget)
		else:#change existing widget
			self.layout.removeWidget(self.widgets[index])
			self.widgets[index] = widget
		self.layout.addWidget(widget, row, col, rowspan, colspan)
		self.raiseOverlay()





	def release(self):
		self._pparent = self.parentWidget()
		self.setParent(None)
		#self.hideTitleBar()


	#def dropEvent(self, ev=None):
		##self.release()
		#
		#self._parent = self.parentWidget()
		##print 11
		#super(nIOpDock,self).dropEvent(ev)
		#print 11,self._parent


	def embedd(self):
		if self._pparent:
			self.setParent(self._pparent)
			#self.showTitleBar()
			self._pparent = None


class DockLabelMenu(QtGui.QMenu):
	
	def __init__(self, dock, *args):
		QtGui.QMenu.__init__(self, *args)
		
		self.dock = dock

		self.action_fullscreen = QtGui.QAction('Fullscreen', self, checkable=True)
		self.addAction(self.action_fullscreen)
		self.action_name = self.addAction('Set Name')

		#connect signals
		self.action_fullscreen.triggered.connect(self.dock.toggleFullscreen)
		self.action_name.triggered.connect(self.setLabelName)

		#enable this menu on right click:
		self.dock.label.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.dock.label,QtCore.SIGNAL('customContextMenuRequested(QPoint)'), self._showContextMenu)

		self.editor = None #set-name-editor


	def setLabelName(self):
		if not self.editor:
			self.editor = QtGui.QLineEdit(self.dock.label)
			self.editor.setText(self.dock.label.text())
			#set smaller size to fit text in label:
			font = QtGui.QFont("Arial", 7)    
			self.editor.setFont(font)
			#transfer text to dockLabel when finished:
			self.editor.editingFinished.connect(self._setLabelNameFinished)
		self.editor.show()


	def _setLabelNameFinished(self):
		self.dock.label.setText(self.editor.text() )
		self.editor.hide()


	def _showContextMenu(self, point):
		self.exec_( self.dock.label.mapToGlobal(point) )



			#self.dock.hide()
			#self.dock.parentWidget().addWidget(self)

# 	def updateStyle(self):
# 		#TODO: über globales menu // self.app weg
# 		r = '3px'
# 		if self.dim or not self.app:
# 			fg = '#aaa'
# 			bg = '#44a'
# 			border = '#339'
# 		else:
# 			fg = self.app.COLOR_FG
# 			bg = self.app.COLOR_BG
# 			border = self.app.COLOR_BORDER
# 		
# 		if self.orientation == 'vertical':
# 			self.vStyle = """DockLabel {
# 				background-color : %s;
# 				color : %s;
# 				border-top-right-radius: 0px;
# 				border-top-left-radius: %s;
# 				border-bottom-right-radius: 0px;
# 				border-bottom-left-radius: %s;
# 				border-width: 0px;
# 				border-right: 2px solid %s;
# 				padding-top: 3px;
# 				padding-bottom: 3px;
# 			}""" % (bg, fg, r, r, border)
# 			self.setStyleSheet(self.vStyle)
# 		else:
# 			self.hStyle = """DockLabel {
# 				background-color : %s;
# 				color : %s;
# 				border-top-right-radius: %s;
# 				border-top-left-radius: %s;
# 				border-bottom-right-radius: 0px;
# 				border-bottom-left-radius: 0px;
# 				border-width: 0px;
# 				border-bottom: 2px solid %s;
# 				padding-left: 3px;
# 				padding-right: 3px;
# 			}""" % (bg, fg, r, r, border)
# 			self.setStyleSheet(self.hStyle)

if __name__ == '__main__':
	import sys
	from fancywidgets import DockArea
	app = QtGui.QApplication(sys.argv)
	win = QtGui.QMainWindow()
	area = DockArea()

	win.setCentralWidget(area)#self.area)
	d = Dock('one')#TODO: fold/unfold
	area.addDock(d)
	win.show()
	sys.exit(app.exec_())

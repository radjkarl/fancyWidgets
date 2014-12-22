# -*- coding: utf-8 -*-
import pyqtgraph.dockarea as pgDock
from pyqtgraph.Qt import QtGui, QtCore


class Dock(pgDock.Dock):
	'''
	added function: 
	
	* setWidget
	* fullscreen in right click menu of label
	* rename in right click menu of label
	* embedd/release to (temporary) free the Dock from its parent DockArea
	'''
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
		else:
			self.release()
			self.showFullScreen()


	def setWidget(self, widget, index=0, row=None, col=0, rowspan=1, colspan=1):
		"""
		Add new widget inside dock, remove old one if existent
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


	def setName(self, name):
		self.label.setText(name)


	def release(self):
		if self.area:
			self._saved_state = self.area.saveState()
		self._pparent = self.parentWidget()
		self.setParent(None)
		self.label.showControls(False)


	def embedd(self):
		if self._pparent:
			self.setParent(self._pparent)
			self._pparent = None
		if self._saved_state:
			self.area.addDock(self)
			self.area.restoreState(self._saved_state)
			self._saved_state = None
		self.checkShowControls()



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
		self.dock.setName(self.editor.text())
		self.editor.hide()


	def _showContextMenu(self, point):
		self.exec_( self.dock.label.mapToGlobal(point) )


if __name__ == '__main__':
	import sys
	from fancywidgets.pyqtgraphBased.DockArea import DockArea
	app = QtGui.QApplication(sys.argv)
	win = QtGui.QMainWindow()
	win.setWindowTitle('Dock')

	area = DockArea()

	win.setCentralWidget(area)
	d = Dock('one')
	area.addDock(d)
	win.show()
	app.exec_()

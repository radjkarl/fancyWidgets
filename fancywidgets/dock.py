# -*- coding: utf-8 -*-
from pyqtgraph.dockarea.Dock import DockLabel as pgDockLabel
from pyqtgraph.dockarea.DockDrop import DockDrop as pgDockDrop

import pyqtgraph.dockarea as pgDock
#-> docks müssen beim speichern berücksichtigt werden
#-> doppelclick fährt docks ein

from QtRec.QtGui import QWidget

pgDock.Dock.__bases__ = (QWidget, pgDockDrop)
class Dock(pgDock.Dock):
	'''adding function: setWidget to normal Dock-class'''
	print pgDock.Dock.__bases__
	def __init__(self, name, app=None, area=None, size=(1,1), widget=None, hideTitle=False, autoOrientation=False):
		super(Dock, self).__init__(name, area, size, widget, hideTitle, autoOrientation)
		self._pparent = None
		self.app = app
		self.label = DockLabel(name, self, app=self.app)





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
		self.hideTitleBar()


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
			self.showTitleBar()
			self._pparent = None


class DockLabel(pgDockLabel):
	
	def __init__(self, text, dock, app=None):
		self.app = app
		pgDockLabel.__init__(self, text, dock)


	#def mouseDoubleClickEvent(self, ev):
		#if ev.button() == QtCore.Qt.LeftButton:
			#self.dock.hide()
			#self.dock.parentWidget().addWidget(self)

	def updateStyle(self):
		r = '3px'
		if self.dim or not self.app:
			fg = '#aaa'
			bg = '#44a'
			border = '#339'
		else:
			fg = self.app.COLOR_FG
			bg = self.app.COLOR_BG
			border = self.app.COLOR_BORDER
		
		if self.orientation == 'vertical':
			self.vStyle = """DockLabel {
				background-color : %s;
				color : %s;
				border-top-right-radius: 0px;
				border-top-left-radius: %s;
				border-bottom-right-radius: 0px;
				border-bottom-left-radius: %s;
				border-width: 0px;
				border-right: 2px solid %s;
				padding-top: 3px;
				padding-bottom: 3px;
			}""" % (bg, fg, r, r, border)
			self.setStyleSheet(self.vStyle)
		else:
			self.hStyle = """DockLabel {
				background-color : %s;
				color : %s;
				border-top-right-radius: %s;
				border-top-left-radius: %s;
				border-bottom-right-radius: 0px;
				border-bottom-left-radius: 0px;
				border-width: 0px;
				border-bottom: 2px solid %s;
				padding-left: 3px;
				padding-right: 3px;
			}""" % (bg, fg, r, r, border)
			self.setStyleSheet(self.hStyle)



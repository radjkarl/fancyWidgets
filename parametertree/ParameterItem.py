# -*- coding: utf-8 -*-

from pyqtgraph.parametertree.ParameterItem import ParameterItem as OldPI
from pyqtgraph.Qt import QtGui, QtCore

import os, nIOp

class ParameterItem(OldPI):
	
	def __init__(self, param, depth=0):
		super(ParameterItem, self).__init__(param, depth)

		if param.opts.get('duplicatable', False):
			self.contextMenu.addAction("Duplicate").triggered.connect(param.duplicate)
		if param.opts.get('type')=='group' or param.opts.get('isGroup', False):
			self.updateDepth(depth)

		icon = param.opts.get('icon', False)
		#if not icon:
			#try:
				#icon = param.opts.get('master', False).icon
			#except:
				#pass
		if icon:
			iconpath = os.path.join(os.path.dirname(nIOp.__file__), icon)
			i = QtGui.QIcon(iconpath)
			self.setIcon(0, i)

		#tip = param.opts.get('tip', False)
		#if tip:
		#	w.setToolTip(tip)


	def childRemoved(self, param, child):
		for i in range(self.childCount()):
			item = self.child(i)
			try:
				# quit and dirty fix:
				# all postprocesses have items of QTreeWidgetItem which don't have .param
				# I dont know why ... but ignoring them allows me to make them removable
				if item.param is child:
					self.takeChild(i)
					break
			except:
				pass


	def updateDepth(self, depth):
		## Change item's appearance based on its depth in the tree
		## This allows highest-level groups to be displayed more prominently.
		if depth == 0:
			for c in [0,1]:
				self.setBackground(c, QtGui.QBrush(QtGui.QColor(100,100,100)))
				self.setForeground(c, QtGui.QBrush(QtGui.QColor(220,220,255)))
				font = self.font(c)
				font.setBold(True)
				font.setPointSize(font.pointSize()+1)
				self.setFont(c, font)
				self.setSizeHint(0, QtCore.QSize(0, 25))
		else:
			for c in [0,1]:
				self.setBackground(c, QtGui.QBrush(QtGui.QColor(220,220,220)))
				font = self.font(c)
				font.setBold(True)
				#font.setPointSize(font.pointSize()+1)
				self.setFont(c, font)
				self.setSizeHint(0, QtCore.QSize(0, 20))



	def columnChangedEvent(self, col):
		"""Exact copy of pyqtgraphs-original only str() with unicode() replaced
		"""
		if col == 0:
			if self.ignoreNameColumnChange:
				return
			try:##EDIT:str() to unicode()
				newName = self.param.setName(unicode(self.text(col)))
			except:
				self.setText(0, self.param.name())
				raise
				
			try:
				self.ignoreNameColumnChange = True
				self.nameChanged(self, newName)  ## If the parameter rejects the name change, we need to set it back.
			finally:
				self.ignoreNameColumnChange = False




	#def text(self,col):
		#return self._text


	#def setText(self,pos, name):
		##limit max len of the paramters name
		#self._text = name
		#if len(name) > 9:
			#name = name[:9] + '\n' + name[9:]
		#print pos,name, type(name)
		#
		#super(ParameterItem,self).setText(pos,'1')
# -*- coding: utf-8 -*-

from pyqtgraph_karl.parametertree.ParameterItem import ParameterItem as OldPI
#from pyqtgraph.parametertree.parameterTypes import ActionParameter

from pyqtgraph_karl.Qt import QtGui, QtCore


class ParameterItem(OldPI):
	
	def __init__(self, param, depth=0):
		#SLIDING
		if param.opts.get('sliding', False):
			self.controls = QtGui.QWidget()
			btnlayout = QtGui.QVBoxLayout() 
			btnlayout.setContentsMargins(0, 0, 0, 0)
			btnlayout.setSpacing(0)
			self.controls.setLayout(btnlayout)
			slideBtnUp = QtGui.QPushButton()
			slideBtnDown = QtGui.QPushButton()
			for btn in (slideBtnUp, slideBtnDown):
				btn.setFixedWidth(10)
				btn.setFixedHeight(10)
				btnlayout.addWidget(btn)
			slideBtnUp.setIcon(QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_ArrowUp))
			slideBtnDown.setIcon(QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_ArrowDown))
			slideBtnUp.clicked.connect(lambda: self.slideChild(-1))#param.slide(-1))
			slideBtnDown.clicked.connect(lambda: self.slideChild(1))#param.slide(1))

		super(ParameterItem, self).__init__(param, depth)

		#DUPLICABILITY
		if param.opts.get('duplicatable', False):
			self.contextMenu.addAction("Duplicate").triggered.connect(param.duplicate)
		if param.opts.get('type')=='group' or param.opts.get('isGroup', False):
			self.updateDepth(depth)
		#ICON
		iconpath = param.opts.get('icon', False)
		if iconpath:
			#iconpath = os.path.join(os.path.dirname(nIOp.__file__), icon)
			i = QtGui.QIcon(iconpath)
			self.setIcon(0, i)
		#TOOLTIP
		#TODO: test
		tip = param.opts.get('tip', False)
		if tip:
			self.setToolTip(0, tip)
		#KEYBOARD SHORTCUT
		self.key = None
		self.setShortcut( param.opts.get('key'), param.opts.get('keyParent'))


	def setShortcut(self, key, parent):
		if key:
			#works for either Action or WidgetParameter
# 			widget = getattr(self, 'button', None)
# 			if not widget:
# 				widget = self.widget

			k = QtGui.QShortcut(parent)#QtGui.QApplication.instance())
			if not isinstance(key, QtGui.QKeySequence):
				key = QtGui.QKeySequence(key)
			k.setKey(QtGui.QKeySequence(key))
			#self.session.gui.shortcuts[key.toString()] = self
			k.setContext(QtCore.Qt.ApplicationShortcut)
			#print isinstance(self.param, ActionParameter), self.param.__class__.__name__
			#if isinstance(self.param, ActionParameter):
			try:
				#for ActionParameter
				k.activated.connect(self.param.activate)
			except AttributeError:
				#toggle
				k.activated.connect(lambda:self.param.setValue(not self.param.value()))
			self.key = k


	def slideChild(self, nPos):
		c = self.treeWidget().currentItem()
		for n in range(self.childCount ()):
			if c == self.child(n):
				c.param.slide(nPos)
				cnew  = self.child(n+nPos)
				return self.treeWidget().setCurrentItem(cnew, 0)
		#self.treeWidget().setCurrentItem(c, 0)
		


	def treeWidgetChanged(self):
		super(ParameterItem, self).treeWidgetChanged()
		if self.param.opts.get('sliding', False):
			t = self.treeWidget()
			i = t.itemWidget(self,0)
			if i is None:
				t.setItemWidget(self, 0, self.controls)
				#move the name a bit
				#if self.text(0)
				#self._setTextSliding(0,self.text(0))
			else:
				#TODO: does this work??
				i.insertWidget(0,self.controls)

# 	def _setTextSliding(self, index, text):
# 		print index, text,99999999999
# 		#if there are sliding arrows at the left: move the item text a bit
# 		if index == 0:
# 			return OldPI.setText(self, index, '  %s'%text)
# 		return OldPI.setText(self, index, text)

	#WHERE DID THAT COME FROM???
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


# 	def childRemoved(self, param, child):
# 		for i in range(self.childCount()):
# 			item = self.child(i)
# 			try:
# 				# quit and dirty fix:
# 				# all postprocesses have items of QTreeWidgetItem which don't have .param
# 				# I dont know why ... but ignoring them allows me to make them removable
# 				if item.param is child:
# 					self.takeChild(i)
# 					break
# 			except:
# 				pass




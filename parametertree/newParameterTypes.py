# -*- coding: utf-8 *-*


from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.python2_3 import asUnicode
from .Parameter import Parameter, registerParameterType
from .ParameterItem import ParameterItem
###########
from .parameterTypes import *
import numpy as np

#from nIOp import _utils
from appBase.aBcollections import NestedOrderedDict
import nIOp #needed for nestedParam - limit finder
import os
import inspect
from nIOp.widgets.table import nIOpTableWidget



class GroupParameterItem(ParameterItem):
	"""
	Group parameters are used mainly as a generic parent item that holds (and groups!) a set
	of child parameters. It also provides a simple mechanism for displaying a button or combo
	that can be used to add new parameters to the group.
	"""
	def __init__(self, param, depth):
		ParameterItem.__init__(self, param, depth)
		self.updateDepth(depth)
		self.addItem = None
		l = param.opts.get('limits', None)
		if l!=None:
			#addText = param.value()#param.opts['value']
		#	if len(l) > 1: #or 'getLimits' in param.opts:
			self.addWidget = QtGui.QComboBox()
			self.addWidget.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
			#self.updateLimits()
			self.addWidget.currentIndexChanged.connect(self.addChanged)
			#self.addChanged()
			#else:
			#	self.addWidget = QtGui.QPushButton(l[0])
			#	self.addWidget.clicked.connect(self.addClicked)
					#self.param.sigLimitsChanged.connect(self.updateLimits)
			self.updateLimits()
			w = QtGui.QWidget()
			l = QtGui.QHBoxLayout()
			l.setContentsMargins(0,0,0,0)
			w.setLayout(l)
			l.addWidget(self.addWidget)
			l.addStretch()
			#l.addItem(QtGui.QSpacerItem(200, 10, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum))
			self.addWidgetBox = w
			self.addItem = QtGui.QTreeWidgetItem([])
			self.addItem.setFlags(QtCore.Qt.ItemIsEnabled)
			ParameterItem.addChild(self, self.addItem)			#self.limitsChanged = self.updateLimits
			self.param.sigLimitsChanged.connect(self.updateLimits)



	#def updateDepth(self, depth):
		### Change item's appearance based on its depth in the tree
		### This allows highest-level groups to be displayed more prominently.
		#if depth == 0:
			#for c in [0,1]:
				#self.setBackground(c, QtGui.QBrush(QtGui.QColor(100,100,100)))
				#self.setForeground(c, QtGui.QBrush(QtGui.QColor(220,220,255)))
				#font = self.font(c)
				#font.setBold(True)
				#font.setPointSize(font.pointSize()+1)
				#self.setFont(c, font)
				#self.setSizeHint(0, QtCore.QSize(0, 25))
		#else:
			#for c in [0,1]:
				#self.setBackground(c, QtGui.QBrush(QtGui.QColor(220,220,220)))
				#font = self.font(c)
				#font.setBold(True)
				##font.setPointSize(font.pointSize()+1)
				#self.setFont(c, font)
				#self.setSizeHint(0, QtCore.QSize(0, 20))


	def addClicked(self):
		"""Called when "add new" button is clicked
		The parameter MUST have an 'addNew' method defined.
		"""
		typ = asUnicode(self.addWidget.currentText())
		#self.param.opts['limits'][0] = typ
		self.param.opts['value'] = typ

		self.param.sigValueChanged.emit(self, None)
		#self.param.addNew()


	def addChanged(self):
		"""Called when "add new" combo is changed
		The parameter MUST have an 'addNew' method defined.
		"""
		if self.addWidget.currentIndex() == 0:
			return
		typ = asUnicode(self.addWidget.currentText())
		#self.param.opts['limits'][0] = typ
		self.param.opts['value'] = typ
		self.param.sigValueChanged.emit(self, None)

		#self.param.addNew(typ)
		self.addWidget.setCurrentIndex(0)

	def treeWidgetChanged(self):
		ParameterItem.treeWidgetChanged(self)
		self.treeWidget().setFirstItemColumnSpanned(self, True)
		if self.addItem is not None:
			self.treeWidget().setItemWidget(self.addItem, 0, self.addWidgetBox)
			self.treeWidget().setFirstItemColumnSpanned(self.addItem, True)



	def updateLimits(self):
		l = self.param.opts.get('limits')
		#if len(l) == 1:
		#	self.addWidget.activated.connect(self.addClicked)
		
		#else:
			#try:
		#		self.addWidget.activated.disconnect(self.addClicked)
		#	except TypeError:
		#		pass # not connected
		self.addWidget.blockSignals(True)
		if isinstance(self.addWidget, QtGui.QComboBox):
			try:
				self.addWidget.clear()
				try:
					self.addWidget.addItem(self.param.opts['addName'])
				except KeyError:
					pass
				if not l:
					self.addWidget.hide()
				else:
					self.addWidget.show()
				for t in l:#self.param.opts['limits']:
					self.addWidget.addItem(t)
			finally:
				self.addWidget.blockSignals(False)



class GroupParameter(Parameter):
	"""
	Group parameters are used mainly as a generic parent item that holds (and groups!) a set
	of child parameters.

	It also provides a simple mechanism for displaying a button or combo
	that can be used to add new parameters to the group. To enable this, the group
	must be initialized with the 'addText' option (the text will be displayed on
	a button which, when clicked, will cause addNew() to be called). If the 'addList'
	option is specified as well, then a dropdown-list of addable items will be displayed
	instead of a button.
	"""
	itemClass = GroupParameterItem
registerParameterType('group', GroupParameter, override=True)



class EmptyParameter(Parameter):
	"""
	Group parameters are used mainly as a generic parent item that holds (and groups!) a set
	of child parameters.

	It also provides a simple mechanism for displaying a button or combo
	that can be used to add new parameters to the group. To enable this, the group
	must be initialized with the 'addText' option (the text will be displayed on
	a button which, when clicked, will cause addNew() to be called). If the 'addList'
	option is specified as well, then a dropdown-list of addable items will be displayed
	instead of a button.
	"""
	itemClass = ParameterItem
registerParameterType('empty', EmptyParameter, override=True)



class NestedParameterItem(ParameterItem):
	"""
	Group parameters are used mainly as a generic parent item that holds (and groups!) a set
	of child parameters. It also provides a simple mechanism for displaying a button or combo
	that can be used to add new parameters to the group.
	"""
	def __init__(self, param, depth):
		ParameterItem.__init__(self, param, depth)

		self.updateDepth(depth)
		self.addItem = None
		#self._nested = OrderedDict()
		#if isinstance(param.value(), str):
		
		addText = param.opts['addText']#.value()#param.opts['value']
		#if 'limits' in param.opts: #or 'getLimits' in param.opts:
		self.menu = QtGui.QMenuBar()
		self.addWidget = QtGui.QMenu(addText)
		self.menu.addMenu(self.addWidget)
		#self.menu.show()
		#self.menu.menuAction().connect(self.menu.show)
		#self.addWidget.aboutToHide = self.ppp
		self.updateLimits()
		self.addWidgetBox = self.menu
		self.addItem = QtGui.QTreeWidgetItem([])
		self.addItem.setFlags(QtCore.Qt.ItemIsEnabled)
		ParameterItem.addChild(self, self.addItem)
		
		#self.limitsChanged = self.updateLimits
		self.param.sigLimitsChanged.connect(self.updateLimits)



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

	#def addClicked(self):
		#"""Called when "add new" button is clicked
		#The parameter MUST have an 'addNew' method defined.
		#"""
		#self.param.sigValueChanged.emit(self, None)
		##self.param.addNew()

	#def addChanged(self):
		#"""Called when "add new" combo is changed
		#The parameter MUST have an 'addNew' method defined.
		#"""
		#if self.addWidget.currentIndex() == 0:
			#return
		#typ = asUnicode(self.addWidget.currentText())
		##TODO: sinn von value ('add') bei nested
		#self.param.opts['value'] = typ
		#####
		##self.param.sigValueChanged.emit(self, typ)

		##self.param.addNew(typ)
		#self.addWidget.setCurrentIndex(0)

	def treeWidgetChanged(self):
		ParameterItem.treeWidgetChanged(self)
		self.treeWidget().setFirstItemColumnSpanned(self, True)
		if self.addItem is not None:
			self.treeWidget().setItemWidget(self.addItem, 0, self.addWidgetBox)
			self.treeWidget().setFirstItemColumnSpanned(self.addItem, True)


	def updateLimits(self):
		self._entries = []
		if self.param.opts.get('limits'):

			self.addWidget.blockSignals(True)

			self.addWidget.clear()
			l = self.param.opts['limits']

			if l:
				self._buildRecursive(l, self.addWidget)

		self.addWidget.blockSignals(False)

	def _buildRecursive(self, limitView, menuView):
		if limitView:
			#get a sorted structure:
			for name in sorted(limitView.keys()):
				method = limitView[name]
				iconpath = self.param._icon_dict.get(id(method),None)
				if iconpath:
					iconpath = '%s/%s' %(os.path.dirname(nIOp.__file__), iconpath)
				##else:
				#	iconpath = None
	
				if isinstance(method, NestedOrderedDict):
					submenu = QtGui.QMenu(name)
					if iconpath:
						submenu = menuView.addMenu(QtGui.QIcon(iconpath), name)#submenu)
					else:
						submenu = menuView.addMenu(name)#submenu)
					self._entries.append(submenu)
					self._buildRecursive(method, submenu)
				else:
					entry = menuView.addAction(name)
					if iconpath:
						qIcon = QtGui.QIcon(iconpath)
						entry.setIcon(qIcon)
					entry.triggered.connect(method)


class NestedParameter(Parameter):
	itemClass = NestedParameterItem
	def __init__(self, *args, **kwargs):
		Parameter.__init__(self, *args, **kwargs)
		self._icon_dict = {}

	def moduleStructureToLimits(self, mainModule, callMethod):
		self._callMethod = callMethod
		self.opts['setValue'] = self._setValue
		l = self.opts['limits'] = NestedOrderedDict()
		self._nameToFunc = {}
		self._mainPath = mainModule.__package__
		self._buildLimitsRecursive('', mainModule, l)
		self.setLimits(self.opts['limits'])


	def _buildLimitsRecursive(self,namePath, module, limitView):
		#sys.exit()
		for modName in dir(module):
			try:
				mod = eval('%s.%s' %(module.__name__, modName))
				if modName[0] != '_':
					if inspect.ismodule(mod):
						p = self._mainPath
						if namePath:
							p+='.'+namePath.replace(', ','.')[:-1]
						if mod.__name__.startswith(p):

							#only create a submenu for folders:
							if mod.__package__ == mod.__name__:
								l = limitView[modName] = NestedOrderedDict()
								#namePath += '%s, ' %modName
							else:
								#use same menu for all classes of alle files on one folder
								l = limitView
							self._buildLimitsRecursive(l.path, mod,l)
					else:
						if inspect.isclass(mod) and mod.__module__ == module.__name__:
							#namePath += '%s, ' %modName
							val = '%s, %s' %(limitView.path, modName)
							lambdaFunc = self._createLambda(val)
							limitView[modName] = lambdaFunc

							try:
								self._icon_dict[id(lambdaFunc)] = mod.icon
							#	limitView[modName] = lambdaFunc, mod.icon
							except AttributeError:
								pass
							self._nameToFunc[val] = mod
							#namePath = ''
			except:
				pass


	def _createLambda(self, arg):
		#i dont know why, but if i call lambda in no extra function it wont work
		return lambda: self.__call__(value=arg)




	def _setValue(self, namePath):
		cls = self._nameToFunc[namePath]
		return self._callMethod(cls)
		#return self._nameToFunc[namePath]



	def appendLimits(self, pathStr, name, method=None):
		l = self.opts['limits']
		for member in pathStr.split(','):
			l = l[member]
		if not method:
			#TODO: praent#ordered Dict
			method = NestedOrderedDict()
		l[name] = method
		self.setLimits(self.opts['limits'])



#registerParameterType('structure', StructureParameter, override=True)
registerParameterType('nested', NestedParameter, override=True)









class newListParameterItem(ListParameterItem):
	"""
	debugged
	"""

	def limitsChanged(self, param, limits):
		# set up forward / reverse mappings for name:value
		if len(limits) == 0:
			limits = ['']  ## Can never have an empty list--there is always at least a singhe blank item.
		
		self.forward, self.reverse = ListParameter.mapping(limits)
		try:
			self.widget.blockSignals(True)
			val = self.targetValue  #asUnicode(self.widget.currentText())
			#<<<<NEW
			if val != None:
				# because self.setValue wont be executed every time
				# self.targetValue can sometimes be wrong
				val = param.value()
			#>>>>>
			self.widget.clear()
			for k in self.forward:
				self.widget.addItem(k)
				if k == val:

					self.widget.setCurrentIndex(self.widget.count()-1)
					self.updateDisplayLabel()
		finally:
			self.widget.blockSignals(False)

class newListParameter(ListParameter):
	itemClass = newListParameterItem


registerParameterType('list', newListParameter, override=True)



class ResetListParameterItem(ListParameterItem):
	"""
	a listparameter that allways returning to the first item
	"""
	def __init__(self, param, depth):
		super(ResetListParameterItem,self).__init__(param, depth)
		#the resetList will reset automatically - there is no need for a default button
		self.defaultBtn.hide()


	def valueChanged(self, *args, **kwargs):
		self.widget.setCurrentIndex(0)
		self.targetValue = self.widget.itemText(0)#.currentText()


	def limitsChanged(self, param, limits):
		self.widget.setCurrentIndex(0)
		super(ResetListParameterItem,self).limitsChanged(param, limits)



class ResetListParameter(ListParameter):
	itemClass = ResetListParameterItem
	#def __init__(self, *args, **kwargs):
		#ListParameter.__init__(self, *args, **kwargs)
		#self.defaultBtn.hide()
		#if 'default' not in self.opts:
			#self.opts['default'] = self.opts['limits'][0]
		#print self.opts['default']


registerParameterType('resetList', ResetListParameter, override=True)












class _SubItem(QtGui.QTreeWidgetItem):
#	def __init__(self, *opts):
#		super(_TableSubItem, self).__init__(*opts)
	def selected(self, value):
		#this dummymethod prevent the following error:
			#Traceback (most recent call last):
			#File "/usr/lib/pymodules/python2.7/pyqtgraph/parametertree/ParameterTree.py", line 107, in selectionChanged
			#self.lastSel.selected(False)
			#AttributeError: 'QTreeWidgetItem' object has no attribute 'selected'
		pass


#debugged:
class NewTextParameterItem(TextParameterItem):
	def __init__(self, *opts):
		WidgetParameterItem.__init__(self, *opts)
		#debug
		self.subItem = _SubItem()
		self.addChild(self.subItem)


	def selected(self, value):
		#this dummymethod prevent the following error:
			#Traceback (most recent call last):
			#File "/usr/lib/pymodules/python2.7/pyqtgraph/parametertree/ParameterTree.py", line 107, in selectionChanged
			#self.lastSel.selected(False)
			#AttributeError: 'QTreeWidgetItem' object has no attribute 'selected'
		pass

	def makeWidget(self):
		self.textBox = QtGui.QTextEdit()
		self.textBox.setMaximumHeight(100)
		###fixed string - unicode error:
		self.textBox.value = lambda: unicode(self.textBox.toPlainText())
		###
		self.textBox.setValue = self.textBox.setPlainText
		self.textBox.sigChanged = self.textBox.textChanged
		return self.textBox


class TextParameter(Parameter):
	"""Editable string; displayed as large text box in the tree."""
	itemClass = NewTextParameterItem
registerParameterType('text', TextParameter, override=True)






class TableParameterItem(WidgetParameterItem):
	'''doesnt work at the moment...'''
	def __init__(self, param, depth):

		initTable = param.opts.get('value')
		if initTable:
			self._y = len(initTable[0])
			self._x = len(initTable)
		else:
			self._x = 3
			self._y = 3

		WidgetParameterItem.__init__(self, param, depth)
		#debug:
		self.subItem = _SubItem()
		self.addChild(self.subItem)

		self.param.sigHeaderChanged.connect(self.headerChanged)

		if initTable:
			self.tableBox.importTable(initTable)
		header = self.param.opts.get('header')
		if header:
			self.headerChanged(header)

		colFixed = self.param.opts.get('columnsFixed', False)
		#if colFixed:
		self.tableBox.setColumnsFixed(colFixed)
#		if not param.opts.get('visible',True):
#			self.tableBox.hide()

	#def show(show=True):
		
		#visible = self.param.opts.get('visible', None)
		#if visible != None:
		#	print 11111,visible
	#	self.param.show()
	#	self.param.hide()#visible)
		#self.setHidden(True)

#	def setColumnsFixed(self, value):
	#	self.tableBox.setColumnsFixed(value)

	def limitsChanged(self, param, limits):
		#self._updateSize(limits)#[0],limits[1])
		self.tableBox.setRowCount(limits[1])
		self.tableBox.setColumnCount(limits[0])


	def headerChanged(self, header):
		#print header,88888
		for n,h in enumerate(header):
			item = QtGui.QTableWidgetItem()
			#item.setText(str(h))#QtCore.QString(val))
			item.setText(h)#QtCore.QString(val))

			#print n,h,self.tableBox.horizontalHeaderItem(n)
			self.tableBox.setHorizontalHeaderItem(n,item)


	def treeWidgetChanged(self):
		self.treeWidget().setFirstItemColumnSpanned(self.subItem, True)
		self.treeWidget().setItemWidget(self.subItem, 0, self.tableBox)
		self.setExpanded(True)
		
	def makeWidget(self):
		#init shape
		self.layoutWidget = QtGui.QWidget()
		self.tableBox = nIOpTableWidget(self._x,self._y,self.layoutWidget)
#		self.tableBox.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.MinimumExpanding)
		self.tableBox.horizontalHeader().setStretchLastSection(True)
		for col in range(self.tableBox.columnCount()-1):
			self.tableBox.setColumnWidth(col,50)

		#self.tableBox.setDragEnabled(True)
		self.tableBox.setAcceptDrops(True)


		#self.textBox = QtGui.QTextEdit()
		#self.textBox.setMaximumHeight(100)
		#self.textBox.value = lambda: str(self.textBox.toPlainText())
		#self.textBox.setValue = self.textBox.setPlainText
		#self.tableBox.sigChanged = self.tableBox.cellChanged
		self.layoutWidget.sigChanged = self.tableBox.cellChanged
	#	self.tableBox.setItem(0,0, self.tableBox.item(0,0))
	#	print self.tableBox.currentItem(),445
		#self.setHidden = self.tableBox.hide

		#self.layoutWidget.hide()
		#self.tableBox.hide()
		self.layoutWidget.value = self._getTable#lambda: self.__call__(value=arg)
		#self.layoutWidget.value = self.tableBox.currentItem.text#lambda:
		self.layoutWidget.setValue = self.tableBox.importTable#self.tableBox.currentItem.text#lambda:

		return self.layoutWidget#self.tableBox#.table


	def _getTable(self):
		l = []#rowCount()
		for row in range(self.tableBox.rowCount()):
			l.append([])
			for col in range(self.tableBox.columnCount()):
				item = self.tableBox.item(row,col)
				if item == None:
					text = ''
				else:
					#text = str(item.text())
					text = asUnicode(item.text())
			#	print self.tableBox, self.tableBox.item(row,col), row, col
				l[-1].append(text)
		return l
					#self._notepadItem.setItem(row,col, item)


	
		
class TableParameter(Parameter):
	"""Editable string; displayed as large text box in the tree."""
	itemClass = TableParameterItem
	sigHeaderChanged = QtCore.Signal(object,object)  ## self, {opt:val, ...}
	#sigColumnsFixedChanged = QtCore.Signal(object,object)  ## self, {opt:val, ...}

	def setHeader(self, header):
		#print header,55555
		self.sigHeaderChanged.emit(self, header)

	#def setColumnsFixed(self, value):
	#	self.sigColumnsChanged.emit(self, value)


	def toArray(self, checkAscending=False):
		table =  self.value()
		lenCol = len(table[0])
		for x in range(len(table)-1,-1,-1):
			for y in range(lenCol):
				try:
					table[x][y] = float(table[x][y])
				except:
					#print errm
					table.pop(x)
					break
		if not table:
			raise Exception("table has no valid data")
		if checkAscending:
			#look whether table sorted:
			v0 = table[0][0]
			for n in range(1,len(table),1):
				v1 = table[n][0]
				if v0 > v1:
					raise Exception(
						"table-input has to be in ascending order, see value '%s' at row '%s'"
						%(v1,n+1))
				v0 = v1
		#self._table = np.array(sorted(table))
		return np.array(table)

registerParameterType('table', TableParameter, override=True)

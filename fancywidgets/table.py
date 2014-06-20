# -*- coding: utf-8 -*-
from QtRec import QtGui, QtCore

###########


#from appBase import utils

class _TableMenu(QtGui.QWidget):
	def __init__(self, table):
		QtGui.QWidget.__init__(self)
		self._table = table
		self._menu=QtGui.QMenu(self)
		#size = QtGui.QMenu('')
		#TODO: ctrl+a machen, dann löschen
		#TODO: wie mit bereiten umgehen -wenn diese kopiert oder gelöscht werden??
		self._menu.addAction('Clean').triggered.connect(self._table.cleanTable)
		#size = self._menu.addMenu('Size')
		#size.addAction('add Row').triggered.connect(self._table.addRow)
		#size.addAction('remove Row').triggered.connect(self._table.removeRow)
		#size.addAction('add Column').triggered.connect(self._table.addCol)
		#size.addAction('remove Column').triggered.connect(self._table.removeCol)


	def show(self, evt):
		self._menu.popup(evt.globalPos())



class _HeaderMenu(QtGui.QWidget):
	def __init__(self, header):
		QtGui.QWidget.__init__(self)
		#self._table = table
		self._header = header

	def show(self, evt):
		#print col#, evt
		menu=QtGui.QMenu(self)


		#size = self._menu.addMenu('Sittze')
		menu.addAction('test')#.triggered.connect(self._table.addRow)
		#index = self._header.currentIndex()
		#print self._header.indexWidget(index)
		#print self._table.indexWidget(index)

		#widget = self._table.indexWidget(self._header.currentIndex())
		#globalPos = widget.mapToGlobal(widget.pos())
		#print self._header.indexWidget(self._header.currentIndex())#indexWidget(col)
		menu.popup(evt.globalPos())#evt.globalPos())
		#self._menu.show()


class _Header(QtGui.QHeaderView):
	
	def __init__(self, orientation, parent=None):
		QtGui.QHeaderView.__init__(self, orientation, parent)
		#super(_HeaderMenu, self).__init__(parent)
		self._menu = _HeaderMenu(self)
		self.setResizeMode(QtGui.QHeaderView.Fixed)


	def mousePressEvent(self, evt):
		mouseBtn = evt.button()
		if mouseBtn == QtCore.Qt.RightButton:
			#print 55
			self._menu.show(evt)
		super(_Header, self).mousePressEvent(evt)



#class _TableHistory(object):

	#def __init__(self):
		#self._len_hist = 10
		#self._n = self._len_hist-1
		#self._l = []
		#for i in range(self._len_hist):
			#self._l.append(None)
		#self._len_hist -= 1


	#def newLog(self,method, *args):
		#self._l.append((method,args))
		#self._l.pop(0)
		#self._n = self._len_hist


	#def changeLog(self, method, *args):
		#self._l[self._n] = (method,args)


	#def undo(self):
		#u = self._l[self._n]
		#if u:
			#self._execute(u)
		#if self._n > 0:
			#self._n -= 1


	#def redo(self):
		#if self._n < self._len_hist:
			#self._n += 1
		#u = self._l[self._n]
		#if u:
			#self._execute(u)


	#def _execute(self,u):
			#args = u[1]
			#if not args:
				#return u[0]
			#if len(args) == 1:
				#return u[0](args)
			#return u[0](*args)



class Table(QtGui.QTableWidget):
	def __init__(self, rows=3,cols=3,parent=None):
		super(Table, self).__init__(rows,cols,parent)
		#self._plus = QtGui.QTableWidgetItem('+/-')
		self._menu = _TableMenu(self)
		self._colFixed = False
		self._rowFixed = False
		#self._history = _TableHistory()
		#self.log = self._history.newLog
		#self.changeLog = self._history.changeLog
	#	self.setHorizontalHeader(_Header(QtCore.Qt.Horizontal, self))
		self.setCurrentCell(0,0)
	#	self.itemClicked.connect(self._logItem)
		#self.currentItemChanged.connect(self._ifEmptyCleanTable)
		#self.itemEntered.connect(self._logItem2)
		#self.cellEntered.connect(self._logCellEntry)
		#self.itemChanged.connect(self._logItem)
		self.currentCellChanged.connect(self._ifBorderAddRow)#)
		#k = QtGui.QShortcut(self)
		#k.setKey(QtGui.QKeySequence.MoveToNextLine)
		#k.setContext(QtCore.Qt.ApplicationShortcut)
		#k.activated.connect(self._ifBorderAddRow)

	def _ifBorderAddRow(self,row, column, lastRow, lastColumn):
		if row == self.rowCount()-1:
			if not self._rowFixed:
				self.setRowCount(row+2)
		if column == self.columnCount()-1:
			if not self._colFixed:
				self.setColumnCount(column+2)

		#item = self.item(lastRow,lastColumn)
		#print item
		#last cell is empty / deleted:
		#if item and item.text() == '':
		#	print 55
		#	self.cleanTable()

	#def _logCellEntry(self, row, col):
		#print row,col
		#item = self.itemAt(row,col)
		#try:
			#item.lastText = item.text()
		#except:
			#pass
		##if not item:
			##self._lastEntry = (row,col,'')
		##else:
			##self._lastEntry = (row,col,item.text())
		#
	#def _logItem(self, item):
		#try:
		##print item,888, x
			#self.log(self.setItemText,item.row(),item.column(),item.lastEntry)
		#except:
			#self.log(self.setItemText,item.row(),item.column(),'')


	def mousePressEvent(self, event):
		mouseBtn = event.button()
		if mouseBtn == QtCore.Qt.RightButton:
			#item = self.itemAt(self.event.globalPos())
			#for col in range(self.columnCount()):
				#if self.horizontalHeaderItem(col) == item:
					#self._headerMenu.show()
					#return super(nIOpTableWidget, self).mousePressEvent(event)
			self._menu.show(event)
		super(Table, self).mousePressEvent(event)


	def keyPressEvent(self, event):
		if event.matches(QtGui.QKeySequence.Copy):
			self.copy()
		elif event.matches(QtGui.QKeySequence.Cut):
			self.copy()
			self.delete()
		elif event.matches(QtGui.QKeySequence.ZoomIn):#Ctrl+Plus
			print 'TODO: add Collums/Row'
		elif event.matches(QtGui.QKeySequence.ZoomOut):#Ctrl+Minus
			print 'TODO: remove Collums/Row'
		elif event.matches(QtGui.QKeySequence.Delete):
			self.delete()
		elif event.matches(QtGui.QKeySequence.Paste):
			self.paste()
		#elif event.matches(QtGui.QKeySequence.Undo):
			#self._history.undo()
		#elif event.matches(QtGui.QKeySequence.Redo):
			#self._history.redo()
		else:
			QtGui.QTableWidget.keyPressEvent(self, event)



	#def addRow(self):
		#if not self._rowFixed:
			#c = self.rowCount()
			#self.setRowCount(c+1)
			#self.log(self.setRowCount,c-1)


	#def removeRow(self):
		#if not self._rowFixed:
			#c = self.rowCount()
			#self.setRowCount(c-1)
			#self.log(self.setRowCount,c+1)


	#def addCol(self):
		#if not self._colFixed:
			#c = self.columnCount()
			#self.setColumnCount(c+1)
			#self.log(self.setColumnCount,c-1)


	#def removeCol(self):
		#if not self._colFixed:
			#c = self.columnCount()
			#self.setColumnCount(c-1)
			#self.log(self.setColumnCount,c+1)


	def delete(self):
		for item in self.selectedItems():
			r,c = item.row(), item.column()
			self.takeItem(r,c)
			#self.setItemText(r,c,'')
			#self.log(self.takeItem,r,c)
		self.cleanTable()

	def cleanTable(self):
		r =self.rowCount()
		c = self.columnCount()
		#try to remove empty rows:
		if not self._rowFixed:
			while True:
				for col in range(c):
					isempty=True
					item = self.item(r,col)
					if item and item.text():
						isempty=False
						break
				if isempty:
					self.setRowCount(r)
					if r == 2: #min table resolution:2x2
						break
					r-=1
				else:
					break
		#try to remove empty columns:
		if not self._colFixed:
			while True:
				for row in range(r):
					isempty=True
					item = self.item(row,c)
					if item and item.text():
						isempty=False
						break
				if isempty:
					self.setColumnCount(c)
					if c == 2: #min table resolution:2x2
						break
					c-=1
				else:
					break



	def setColumnsFixed(self, value):
		self._colFixed = value


	def copy(self):
		firstRange = self.selectedRanges()[0]
		#deselect all other ranges, to show shat only the first one will copied
		for otherRange in self.selectedRanges()[1:]:
			self.setRangeSelected(otherRange, False)
		nCols = firstRange.columnCount()
		nRows = firstRange.rowCount()
		if not nCols or not nRows:
			return
		text = ''
		lastRow = nRows+firstRange.topRow()
		lastCol = nCols+firstRange.leftColumn()
		for row in range(firstRange.topRow(), lastRow):
			for col in range(firstRange.leftColumn(), lastCol):
				item = self.item(row, col)
				if item:
					text += str(item.text())
				if col != lastCol-1:
					text += '\t'
			text += '\n'
		QtGui.QApplication.clipboard().setText(text)


	def paste(self):
		#get the text from the clipboard
		text = str(QtGui.QApplication.clipboard().text())
		table = None
		if text.startswith('[[') or text.startswith('(('):
			try:
			#maybe it's already formated as a list e.g. "[['1','2'],[...]]"
			#check it:
				t = eval(text)
			#has to be a 2d-list:
				if isinstance(t, list) and isinstance(t[0],list):
					table = t
			except SyntaxError:
				#not a valid list
				pass
		if not table:
			#create the list from the clipboard-text
			#therefore the text has to be formeted like this:
				# "1\t2\3\n4\t5\6\n"
			table = text.split('\n')
			n = 0
			while n < len(table):
				sline = table[n].split('\t')
				if sline != ['']:
					table[n] = sline
				else:
					table.pop(n)
					n -= 1
				n += 1
		self.importTable(table)


	def importTable(self, table):#, fitShape=True):
		if table:
			r = self.selectedRanges()[0]
			startRow = r.topRow()
			startCol = r.leftColumn()
			lastRow = startRow+len(table)
			lastCol = startCol+len(table[0])
			if not self._rowFixed:
				if self.rowCount() < lastRow:
					self.setRowCount(lastRow)
			if not self._colFixed:
				if self.columnCount() < lastCol:
					self.setColumnCount(lastCol)
			#self.setColumnCount(startCol+len(table[0]))
			for row in range(self.rowCount()):
				for col in range(self.columnCount()):
					try:
						newText = str(table[row][col])
						r,c = row+startRow,col+startCol
						self.setItemText(r,c, newText, True)
					except:
						pass

	def setItemText(self, row, col, text):
		#print row, col
		item = self.item(row,col)
		if not item:
			lasttext = ''
		else:
			lasttext = item.text()
		#if addLog:
		#	self.log(self.setItemText,row,col,lasttext)
		#else:
			#self.changeLog(self.setItemText,row,col,lasttext)
		newItem = QtGui.QTableWidgetItem()
		newItem.setText(text)
		self.setItem(row,col,newItem)
# -*- coding: utf-8 -*-

#own
from PyQt4 import QtGui, QtCore
from fancywidgets.pyQtBased.Dialogs import Dialogs
#foreign
import csv



class Table(QtGui.QTableWidget):
    '''
    A QTableWidget with:
    * Shortcuts: copy, paste, cut, insert/delete row/column
    * Context Menu
    * Cell range operations (copy, paste on multiple cells)
    * Save/open
    * import from clipboard
    * dynamic add of new rows and cells when needed
    '''
    sigPathChanged = QtCore.pyqtSignal(object) # file path

    def __init__(self, rows=3,cols=3, colFiled=False, rowFixed=False, parent=None):
        super(Table, self).__init__(rows,cols,parent)
        self._menu = _TableMenu(self)
        self._colFixed = colFiled
        self._rowFixed = rowFixed
        self._dialogs = Dialogs()

        self._path = None
    #    self.setHorizontalHeader(_Header(QtCore.Qt.Horizontal, self))
        self.setCurrentCell(0,0)
        self.currentCellChanged.connect(self._ifAtBorderAddRow)#)

    def restore(self, path):
        self.clearContents()
        text = open(path,'r').read()
        table = self._textToTable(text, ',')
        self.importTable(table)        

    def open(self, path):
        if not path:
            path = self._dialogs.getOpenFileName(filter='*.csv')
        if path:
            self.restore(path)
            self._setPath(path)


    def _setPath(self, path): 
        self._path = path 
        self.sigPathChanged.emit(path)


    def save(self):
        '''
        save to file - override last saved file
        '''
        self.saveAs(self._path)


    def table(self):
        l = []
        for row in range(self.rowCount()):
            rowdata = []
            for column in range(self.columnCount()):
                item = self.item(row, column)
                if item is not None:
                    rowdata.append(
                        unicode(item.text()).encode('utf8'))
                else:
                    rowdata.append('')    
            l.append(rowdata)
        return l


    def saveAs(self, path):
        '''
        save to file under given name
        '''
        if not path:
            path = self._dialogs.getSaveFileName(filter='*.csv')
        if path:
            self._setPath(path)
            with open(unicode(self._path), 'wb') as stream:
                writer = csv.writer(stream)
                table = self.table()
                for row in table:
                    writer.writerow(row)


    def _ifAtBorderAddRow(self,row, column, lastRow, lastColumn):
        if row == self.rowCount()-1:
            if not self._rowFixed:
                self.setRowCount(row+2)
        if column == self.columnCount()-1:
            if not self._colFixed:
                self.setColumnCount(column+2)


    def mousePressEvent(self, event):
        mouseBtn = event.button()
        if mouseBtn == QtCore.Qt.RightButton:
            self._menu.show(event)
        super(Table, self).mousePressEvent(event)


    def keyPressEvent(self, event):
        if event.matches(QtGui.QKeySequence.Copy):
            self.copy()
        elif event.matches(QtGui.QKeySequence.Cut):
            self.copy()
            self.delete()
        elif event.matches(QtGui.QKeySequence.ZoomIn):#Ctrl+Plus
            self.insertBlankCells()
        elif event.matches(QtGui.QKeySequence.ZoomOut):#Ctrl+Minus
            self.removeBlankCells()
        elif event.matches(QtGui.QKeySequence.Delete):
            self.delete()
        elif event.matches(QtGui.QKeySequence.Paste):
            self.paste()
        else:
            QtGui.QTableWidget.keyPressEvent(self, event)


    def insertBlankCells(self):
        #TODO: insert only cells for selected range
        r = self.selectedRanges()
        if len(r) > 1:
            print 'Cannot insert cells on multiple selections'
            return
        r = r[0]
        if r.leftColumn() == r.rightColumn():
            self.insertColumn(r.leftColumn())
        elif r.leftRow() == r.rightRow():
            self.insertRow(r.leftRow())
        else:
            print 'Need one line of rows or columns to insert blank cells'
            
            
    def removeBlankCells(self):
        #TODO: remove only cells for selected range
        r = self.selectedRanges()
        if len(r) > 1:
            print 'Cannot remove cells on multiple selections'
            return
        r = r[0]
        if r.leftColumn() == r.rightColumn():
            self.removeColumn(r.leftColumn())
        elif r.leftRow() == r.rightRow():
            self.removeRow(r.leftRow())
        else:
            print 'Need one line of rows or columns to insert blank cells'


    def delete(self):
        for item in self.selectedItems():
            r,c = item.row(), item.column()
            self.takeItem(r,c)
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


    def cut(self):
        self.copy()
        self.delete()


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


    def _textToTable(self, text, separator='\t'):
        '''
        format csv, [[...]], ((..)) strings to a 2d table  
        '''
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
            #therefore the text has to be formated like this:
                # "1\t2\3\n4\t5\6\n"
            table = text.split('\n')
            n = 0
            while n < len(table):
                sline = table[n].split(separator)
                if sline != ['']:
                    table[n] = sline
                else:
                    table.pop(n)
                    n -= 1
                n += 1   
        return table    

    
    @staticmethod
    def fromText(text):
        t = Table()
        table = t._textToTable(text)
        if table:
            t.importTable(table)
        else:
            raise Exception('text is no table')
        return t
        

    def paste(self):
        #get the text from the clipboard
        text = str(QtGui.QApplication.clipboard().text())
        if text:
            table = self._textToTable(text)
            self.importTable(table)


    def importTable(self, table, startRow=None, startCol=None):
        if table != None and len(table):
            if startRow is None or startCol is None:
                try:
                    #try to get array to paste in from selection
                    r = self.selectedRanges()[0]
                    startRow = r.topRow()
                    startCol = r.leftColumn()
                except IndexError:
                    startRow = 0
                    startCol = 0
            lastRow = startRow+len(table)
            lastCol = startCol+len(table[0])
            if not self._rowFixed:
                if self.rowCount() < lastRow:
                    self.setRowCount(lastRow)
            if not self._colFixed:
                if self.columnCount() < lastCol:
                    self.setColumnCount(lastCol)
            for row,line in enumerate(table):
                for col, text in enumerate(line):
                    r,c = row+startRow,col+startCol
                    self.setItemText(r,c, unicode(text))


    def setItemText(self, row, col, text):
        item = self.item(row,col)
        if not item:
            item = QtGui.QTableWidgetItem()
            self.setItem(row,col,item)
        item.setText(text)




class _TableMenu(QtGui.QWidget):
    def __init__(self, table):
        QtGui.QWidget.__init__(self)
        self._table = table
        self._menu=QtGui.QMenu(self)

        a = self._menu.addAction('Clean')
        a.triggered.connect(self._table.cleanTable)
        
        self._menu.addSeparator()
        
        a = self._menu.addAction('Copy')
        a.triggered.connect(self._table.copy)
        a.setShortcuts(QtGui.QKeySequence.Copy)

        a  = self._menu.addAction('Paste')
        a.triggered.connect(self._table.paste)
        a.setShortcuts(QtGui.QKeySequence.Paste)

        a  = self._menu.addAction('Cut')
        a.triggered.connect(self._table.cut)
        a.setShortcuts(QtGui.QKeySequence.Cut)
        
        self._menu.addSeparator()

        a  = self._menu.addAction('Insert row/column')
        a.triggered.connect(self._table.insertBlankCells)
        a.setShortcuts(QtGui.QKeySequence.ZoomIn)
        
        a  = self._menu.addAction('Remove row/column')
        a.triggered.connect(self._table.removeBlankCells)
        a.setShortcuts(QtGui.QKeySequence.ZoomOut)
        
        self._menu.addSeparator()

        self._menu.addAction('Open').triggered.connect(self._table.open)
        self._menu.addAction('Save').triggered.connect(self._table.save)
        self._menu.addAction('Save As').triggered.connect(self._table.saveAs)


    def show(self, evt):
        self._menu.popup(evt.globalPos())



# class _HeaderMenu(QtGui.QWidget):
#     '''an individual header menu for QTableWidgets
#      - not used at the moment'''
#     def __init__(self, header):
#         QtGui.QWidget.__init__(self)
#         self._header = header
# 
#     def show(self, evt):
#         menu=QtGui.QMenu(self)
#         menu.addAction('test')#.triggered.connect(self._table.addRow)
#         menu.popup(evt.globalPos())#evt.globalPos())
# 
# 
# class _Header(QtGui.QHeaderView):
#     '''an individual header for QTableWidgets enables a 
#     context menu on right click 
#     - not used at the moment'''
# 
#     def __init__(self, orientation, parent=None):
#         QtGui.QHeaderView.__init__(self, orientation, parent)
#         self._menu = _HeaderMenu(self)
#         self.setResizeMode(QtGui.QHeaderView.Fixed)
# 
# 
#     def mousePressEvent(self, evt):
#         mouseBtn = evt.button()
#         if mouseBtn == QtCore.Qt.RightButton:
#             #print 55
#             self._menu.show(evt)
#         super(_Header, self).mousePressEvent(evt)




if __name__ == '__main__':    
    import sys

    app = QtGui.QApplication(sys.argv)
    w = Table(rows=10,cols=10)
    w.setWindowTitle(w.__class__.__name__)
    w.show()
   
    app.exec_()
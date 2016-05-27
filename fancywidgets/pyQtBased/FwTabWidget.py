# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore



class FwTabWidget(QtGui.QTabWidget):
    '''
    * allow to iterate over all tabs using for tab in TabWidget...
    * allow to give tabs (and not indexes) to:
        * removeTab
        * tabText
    also: interactive...
    * adding of new tabs,
    * tab removal
    * tab renaming
    '''

    sigTabAdded = QtCore.pyqtSignal(object)#tab

    def __init__(self, defaultTabWidget=QtGui.QWidget):
        QtGui.QTabWidget.__init__(self)
        #use lambda to make later overwriting possible:
        self.tabCloseRequested.connect(lambda index: self.removeTab(index))
        self.setTabBar(_TabBar())
        self._btn_add_height = None
        self.defaultTabWidget = defaultTabWidget
        

    def setTabsRenamable(self, renamable):
        self.tabBar().tabsRenamable = renamable


    def setTabsAddable(self, addable):
        if addable:
            btn = QtGui.QToolButton(self)
            btn.clicked.connect(lambda checked: self.addEmptyTab())
            btn.setIcon(QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_FileDialogNewFolder))
            self.setCornerWidget(btn)
            self.tabCloseRequested.connect(self._mkAddBtnVisible)
            self._mkAddBtnVisible() 
        else:
            btn = self.cornerWidget()
            if btn:
                btn.hide()
                self.tabCloseRequested.disconnect(self._mkAddBtnVisible) 

    
    def addEmptyTab(self, text=''):
        '''
        Add a new DEFAULT_TAB_WIDGET, open editor to set text if no text is given 
        '''
        tab = self.defaultTabWidget()
        c = self.count()
        self.addTab(tab, text)
        self.setCurrentIndex (c)
        if not text:
            self.tabBar().editTab(c)
        self.sigTabAdded.emit(tab)
        return tab
       
        
    def _mkAddBtnVisible(self):
        '''
        Ensure that the Add button is visible also when there are no tabs
        '''
        if not self._btn_add_height:
            self._btn_add_height = self.cornerWidget().height()
        if self.count() == 0:
            self.cornerWidget().setMinimumHeight(self._btn_add_height-8)
            self.setMinimumHeight(self._btn_add_height)


    def __iter__(self):
        self._i = -1
        return self
    
    
    def next(self):
        self._i += 1
        if self._i == self.count():
            raise StopIteration()
        return self.widget(self._i)
    
    
    def widgetByName(self, name):
        for i in range(self.count()):
            if self.tabText(i)==name:
                return self.widet(i)
        
        
    def removeTab(self, tab):
        '''allows to remove a tab directly -not only by giving its index'''
        if type(tab) != int:
            tab = self.indexOf(tab)
        return super(FwTabWidget, self).removeTab(tab)


    def tabText(self,tab):
        ''' allow index or tab widget instance'''
        if type(tab) != int:
            tab = self.indexOf(tab)
        return super(FwTabWidget, self).tabText(tab)





class _TabBar(QtGui.QTabBar):
    '''
    allow change of tabTitle via double click
    '''
    def __init__(self, parent=None):
        QtGui.QTabBar.__init__(self, parent)
        
        self.tabsRenamable = False
        
        self._editor = QtGui.QLineEdit(self)
        self._editor.setWindowFlags(QtCore.Qt.Popup)
        self._editor.setFocusProxy(self)
        self._editor.editingFinished.connect(self.handleEditingFinished)
        self._editor.installEventFilter(self)


    def eventFilter(self, widget, event):
        if ((event.type() == QtCore.QEvent.MouseButtonPress and
             not self._editor.geometry().contains(event.globalPos())) or
            (event.type() == QtCore.QEvent.KeyPress and
             event.key() == QtCore.Qt.Key_Escape)):
            self._editor.hide()
            return True
        return QtGui.QTabBar.eventFilter(self, widget, event)


    def mouseDoubleClickEvent(self, event):
        if self.tabsRenamable:
            index = self.tabAt(event.pos())
            if index >= 0:
                self.editTab(index)


    def editTab(self, index):
        rect = self.tabRect(index)
        self._editor.setFixedSize(rect.size())
        self._editor.move(self.parent().mapToGlobal(rect.topLeft()))
        self._editor.setText(self.tabText(index))
        if not self._editor.isVisible():
            self._editor.show()


    def handleEditingFinished(self):
        index = self.currentIndex()
        if index >= 0:
            self._editor.hide()
            self.setTabText(index, self._editor.text())



 
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    w = FwTabWidget()
    w.setWindowTitle(w.__class__.__name__)

    #switching on/off/on
    w.setTabsAddable(True)
    w.setTabsClosable(True)
    w.setTabsRenamable(True)

    w.setTabsAddable(False)
    w.setTabsClosable(False)
    w.setTabsRenamable(False)

    w.setTabsAddable(True)
    w.setTabsClosable(True)
    w.setTabsRenamable(True)
 
    w.show()
    app.exec_()

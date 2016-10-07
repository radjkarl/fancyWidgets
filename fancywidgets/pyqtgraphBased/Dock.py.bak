# -*- coding: utf-8 -*-
import pyqtgraph_karl.dockarea as pgDock
from pyqtgraph_karl.Qt import QtGui, QtCore
import weakref



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
                closable=True, minimizable=True, maximizable=True
                ):
        super(Dock, self).__init__(name, area, size, widget, hideTitle, 
                                autoOrientation, closable, minimizable, maximizable)
        self._pparent = None
        self._saved_state = None

        self.label.menu = DockLabelMenu(weakref.proxy(self))
        #full screen on double click rather than floating dock:
        self.label.mouseDoubleClickEvent = lambda evt: self.setFullscreen()#)evt.ignore()
 

    def close(self):
        f = self.isFullScreen() 
        if f:
            #otherwise wont be close from fullscreen
            self.embedd()
            self.showNormal()
        pgDock.Dock.close(self)
        if f:
            QtGui.QWidget.close(self)


    def closeEvent(self, evt):
        #ignore ALT+F4 if in full screen
        evt.ignore()

  
    def setFullscreen(self):
        if not self.isFullScreen():
            d = QtGui.QApplication.desktop()
            n = d.screenNumber(self)
            self.release()
            #go to current screen:
            self.setGeometry(d.screenGeometry(n))  
            self.showFullScreen()
            self.hideTitleBar()
            #have to add to self in order not to be removed by garbage collector:
            self._fc_msg  = FullscreenMsg(self)



    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            if self.isFullScreen():
                self.embedd()
                self.showNormal()
                self.showTitleBar()
                self._fc_msg.hide()
                


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
        self.label.showControls(True)
        self.checkShowControls()



class FullscreenMsg(QtGui.QLabel):
    '''
    Simple message on top of this window
    hides itself after few seconds
    '''
    def __init__(self, parent):
        QtGui.QLabel.__init__(self, 'Press <ESC> to exit full screen', parent=parent)
        #make frameles:
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setStyleSheet("QLabel { background-color : black; color : white; }")

        QtCore.QTimer.singleShot(3000, self.hide)

        self.move(100,30 ) 
        self.show()



class DockLabelMenu(QtGui.QMenu):
    
    def __init__(self, dock, *args):
        QtGui.QMenu.__init__(self, *args)
        
        self.dock = dock

        self.action_popout = QtGui.QAction('Pop out', self, checkable=True)
        self.addAction(self.action_popout)

        self.action_fullscreen = QtGui.QAction('Fullscreen (double click)', self)#, checkable=True)
        self.addAction(self.action_fullscreen)
        
        self.action_name = self.addAction('Set Name')

        #connect signals
        self.action_fullscreen.triggered.connect(self._fullscreen)
        self.action_popout.triggered.connect(self._popout)

        self.action_name.triggered.connect(self.setLabelName)

        #enable this menu on right click:
        self.dock.label.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self.dock.label,QtCore.SIGNAL('customContextMenuRequested(QPoint)'), self._showContextMenu)

        self.editor = None #set-name-editor


    def _fullscreen(self):
        d = self.dock
        self.action_popout.setEnabled(not d.isFullScreen())
        d.setFullscreen()


    def _popout(self,checked):
        d = self.dock
        if checked:
            d.release()
            d.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
            #BACKUP:
            self._back_mouseMoveEvent = d.label.mouseMoveEvent
            self._back_mouseReleaseEvent = d.label.mouseReleaseEvent
            #MAKE DOCK DRAGABLE:
            d.label.mouseMoveEvent = self._mouseMoveEvent
            d.label.mouseReleaseEvent = self._mouseReleaseEvent
    
            d.show()  
        else:
            l = d.label
            d.embedd()
            #RESTORE:
            l.mouseMoveEvent = self._back_mouseMoveEvent
            l.mouseReleaseEvent = self._back_mouseReleaseEvent
            del self._back_mouseMoveEvent
            del self._back_mouseReleaseEvent


    def _mouseMoveEvent(self, ev):
        d = self.dock
        d.move(ev.globalPos()-d.label.pressPos)

             
    def _mouseReleaseEvent(self, ev):
        pass



    def setLabelName(self):
        if not self.editor:
            self.editor = QtGui.QLineEdit(self.dock.label)
            self.editor.setText(self.dock.label.text())
            #set smaller size to fit text in label:
            font = QtGui.QFont("Arial", 7)    
            self.editor.setFont(font)
            #transfer text to dockLabel when finished:
            self.editor.editingFinished.connect(self._setLabelNameFinished)

        self.editor.move(self.dock.label.width()/2-45,0)
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

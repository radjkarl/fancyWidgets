# -*- coding: utf-8 -*-

#foreign
from PyQt4 import QtGui
from PyQt4.QtCore import Qt
#this pkg
from _textEditorUtils import ToolBarEdit, ToolBarFormat, ToolBarFont


class _TextEdit(QtGui.QTextEdit):
    '''
    allow to show/hide the toolbar through context menu
    '''
    def __init__(self, editor):
        self.editor = editor
        QtGui.QTextEdit.__init__(self, editor)
        self._showToolbarChecked = True
        
        
    def contextMenuEvent(self, event):
        menu = QtGui.QTextEdit.createStandardContextMenu(self)
        menu.addSeparator()

        a = QtGui.QAction('Show Toolbar', menu)
        a.triggered.connect(self.editor.showToolbar)
        a.triggered.connect(self._storeActionValueToolbarChecked)
        a.setCheckable(True)
        a.setChecked(self._showToolbarChecked)
        menu.addAction(a)
        
        menu.exec_(event.globalPos())
        
        
    def _storeActionValueToolbarChecked(self, checked):
        self._showToolbarChecked = checked




class FwTextEditor(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self,parent)
        self.setWindowFlags(Qt.Widget) #allow to use mainwindow as widget

        self.text = _TextEdit(self)

        self.text.setTabStopWidth(12)
        self.setCentralWidget(self.text)
        self.toolbar_edit = ToolBarEdit(self.text)
        self.addToolBar(self.toolbar_edit)
        self.addToolBarBreak()
        t_font = ToolBarFont(self.text)
        self.addToolBar(t_font)
        self.addToolBarBreak()
        t_format = ToolBarFormat(self.text)
        self.addToolBar(t_format)
        
        self.toolbars = [self.toolbar_edit, t_font, t_format]

        self.setGeometry(100,100,700,700)


    def showToolbar(self, show):
        for t in self.toolbars:
            if show:
                t.show()
            else:
                t.hide()
                


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    w= FwTextEditor()
    w.setWindowTitle(w.__class__.__name__)
    w.show()
    app.exec_()
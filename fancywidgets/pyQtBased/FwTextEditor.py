'''
Created on 20 Jun 2014

@author: elkb4
'''
# -*- coding: utf-8 -*-

#foreign
from PyQt4 import QtGui
from PyQt4.QtCore import Qt
#own
from _textEditorUtils import ToolBarEdit, ToolBarFormat, ToolBarFont


class FwTextEditor(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self,parent)
        self.setWindowFlags(Qt.Widget) #allow to use mainwindow as widget

        self.text = QtGui.QTextEdit(self)

        self.text.setTabStopWidth(12)
        self.setCentralWidget(self.text)
        self.toolbar_edit = ToolBarEdit(self.text)
        self.addToolBar(self.toolbar_edit)
        self.addToolBarBreak()
        self.addToolBar(ToolBarFont(self.text))
        self.addToolBarBreak()
        self.addToolBar(ToolBarFormat(self.text))

        self.setGeometry(100,100,700,700)


#------- Statusbar ------------------------------------
        #self.status = self.statusBar()
        #self.text.cursorPositionChanged.connect(self.CursorPosition)

        #self.setMenuBar(TextExitorMenuBar(self))


#-------- Toolbar slots -----------------------------------



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    editor= FwTextEditor()
    editor.show()
    sys.exit(app.exec_())
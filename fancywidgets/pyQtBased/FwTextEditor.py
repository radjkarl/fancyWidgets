# -*- coding: utf-8 -*-

#foreign
from PyQt4 import QtGui
from PyQt4.QtCore import Qt
#this pkg
from _textEditorUtils import ToolBarEdit, ToolBarFormat, ToolBarFont, ToolBarInsert, MainWindow




class FwTextEditor(MainWindow):

    def __init__(self, parent=None):
        MainWindow.__init__(self,parent)

        self.toolbar_edit = ToolBarEdit(self.text)
        self.addToolBar(self.toolbar_edit)
        t_insert = ToolBarInsert(self.text)
        self.addToolBar(t_insert)
        self.addToolBarBreak()
        t_font = ToolBarFont(self.text)
        self.addToolBar(t_font)
        self.addToolBarBreak()
        t_format = ToolBarFormat(self.text)
        self.addToolBar(t_format)

        #self.toolbars = [self.toolbar_edit, t_font, t_format, t_insert]

        self.setGeometry(100,100,700,700)



                





if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    w= FwTextEditor()
    w.setWindowTitle(w.__class__.__name__)
    w.show()
    app.exec_()
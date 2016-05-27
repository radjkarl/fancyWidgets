#foreign
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
#this pkg
from _textEditorUtils import ToolBarFormat, ToolBarFont, ToolBarInsert, MainWindow


class FwMinimalTextEditor(MainWindow):


    def __init__(self, parent=None):
        MainWindow.__init__(self,parent)

        self.text.setTabStopWidth(12)
        self.setCentralWidget(self.text)
        self.addToolBar(ToolBarFont(self.text))
        toolBarInsert = ToolBarInsert(self.text)
        self.addToolBar(toolBarInsert)
        self.addToolBarBreak()
        toolBar = ToolBarFormat(self.text)
        self.addToolBar(toolBar)
        
        toolBarInsert.setIconSize(QtCore.QSize(16,16))        
        toolBar.setIconSize(QtCore.QSize(16,16))
        #self.setGeometry(100,100,700,700)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    w = FwMinimalTextEditor()
    w.setWindowTitle(w.__class__.__name__)

    w.show()
    app.exec_()

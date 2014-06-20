#foreign
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
#own
from _textEditorUtils import ToolBarFormat, ToolBarFont


class MinimalTextEditor(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self,parent)
        self.setWindowFlags(Qt.Widget) #allow to use mainwindow as widget

        self.text = QtGui.QTextEdit(self)
        self.text.setTabStopWidth(12)
        self.setCentralWidget(self.text)

        self.addToolBar(ToolBarFont(self.text))
        self.addToolBarBreak()

        toolBar = ToolBarFormat(self.text)
        self.addToolBar(toolBar)
        toolBar.setIconSize(QtCore.QSize(16,16))
        #self.setGeometry(100,100,700,700)
        

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    editor= MinimalTextEditor()
    editor.show()
    sys.exit(app.exec_())

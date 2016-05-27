# -*- coding: utf-8 *-*

from PyQt4 import QtGui



class Console(QtGui.QTextEdit):
    '''
    A simple qWidget with one read-only QTextEdit with a limited number of lines
    to display output generated with messages which 
    print() in black and raise() in red color
    '''
    MAXLINES = 300

    def __init__(self, outputSignal=None, errorSignal=None, *args, **kwargs):
        QtGui.QTextEdit.__init__(self, *args, **kwargs)

        self._red = QtGui.QColor(255,0,0)
        self._black = QtGui.QColor(0,0,0)
        

        self.setReadOnly(True)
        self._format = QtGui.QTextCharFormat()
        # limit text length:
        self.document().setMaximumBlockCount(self.MAXLINES)
        
        self.outputSignal = outputSignal
        self.errorSignal = errorSignal

    
    # disable drag/drop:#doesnt work?   
#     def dragEnterEvent (self, evt):
#         pass
#     def dragLeaveEvent (self, evt):
#         pass
#     def dragMoveEvent (self, evt): 
#         pass
#     def dropEvent (self, evt):
#         pass

        
    def setActive(self):
        if self.outputSignal is not None:
            self.outputSignal.connect(self.addTextOut)
        if self.errorSignal is not None:
            self.errorSignal.connect(self.addTextErr)
            
            
    def setInactive(self):
        try:
            self.outputSignal.disconnect(self.addTextOut)
            self.errorSignal.disconnect(self.addTextErr)
        except TypeError:
            pass # was not connected


    def addTextOut(self, text):
        '''add black text'''
        self._currentColor = self._black
        self.addText(text)


    def addTextErr(self, text):
        '''add red text'''
        self._currentColor = self._red
        self.addText(text)


    def addText(self, text):
        '''append text in the chosen color'''
        #move to the end of the doc
        self.moveCursor(QtGui.QTextCursor.End)
        #insert the text
        self.setTextColor(self._currentColor)
        self.textCursor().insertText(text)


    def __del__(self):
        '''disconnect from output and error signal'''
        self.setInactive()



    def contextMenuEvent(self, event):
        '''
        Add menu action:
        * 'Show line numbers'
        * 'Save to file'
        '''
        menu = QtGui.QTextEdit.createStandardContextMenu(self)
        
        #create max.lines spin box:
        w = QtGui.QWidget()
        l = QtGui.QHBoxLayout()
        w.setLayout(l)
        e = QtGui.QSpinBox()
        e.setRange(1,1e6)
        e.setValue(self.MAXLINES)
        e.valueChanged.connect(self.document().setMaximumBlockCount)
        l.addWidget(QtGui.QLabel('Max. lines'))
        l.addWidget(e)


        #add spinbox to menu:
        a = QtGui.QWidgetAction(self)
        a.setDefaultWidget(w)
        menu.addAction(a)
        
        menu.exec_(event.globalPos())



if __name__ == '__main__':    
    import sys
    from fancytools.utils.StreamSignal import StreamSignal

    app = QtGui.QApplication(sys.argv)

    #create 2 connectable stdout/stderr signals:
    sout = StreamSignal('out')
    serr = StreamSignal('err')
    
    w = Console(sout.message, serr.message)
    w.setWindowTitle(w.__class__.__name__)
    w.setActive()
    w.show()
    
    #print a normal message that will be visible in the shell AND in the console
    print (1,2,3,'test')
    # print an error if button is pressed:
    def printError(evt):
        raise Exception('this is an error test')
    a = QtGui.QPushButton('press for error')
    a.clicked.connect(printError) 

    a.show()
    app.exec_()

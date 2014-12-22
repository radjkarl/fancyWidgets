# -*- coding: utf-8 *-*

#foreign
from PyQt4 import QtGui



class Console(QtGui.QTextEdit):
	

	'''a simple qWidget with one read-only QTextEdit with a limited number of lines
	to display output generated with messages which 
	print() in black and raise() in red color'''

	def __init__(self, outputSignal=None, errorSignal=None, *args, **kwargs):
		MAXLINES = 300
		QtGui.QTextEdit.__init__(self, *args, **kwargs)

		self._red = QtGui.QColor(255,0,0)
		self._black = QtGui.QColor(0,0,0)
		
		self.setReadOnly(True)
		self._format = QtGui.QTextCharFormat()
		# limit text length:
		self.document().setMaximumBlockCount(MAXLINES)
		
		self.outputSignal = outputSignal
		self.errorSignal = errorSignal
		
		if self.outputSignal != None:
			self.outputSignal.connect(self.addTextOut)
		if self.errorSignal != None:
			self.errorSignal.connect(self.addTextErr)
			

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
		if self.outputSignal != None:
			self.outputSignal.disconnect(self.addTextOut)
		if self.errorSignal != None:
			self.errorSignal.disconnect(self.addTextErr)



if __name__ == '__main__':	
	import sys
	from fancytools.utils.StreamSignal import StreamSignal

	app = QtGui.QApplication(sys.argv)

	#create 2 connectable stdout/stderr signals:
	sout = StreamSignal('out')
	serr = StreamSignal('err')
	
	w = Console(sout.message, serr.message)
	w.setWindowTitle(w.__class__.__name__)

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


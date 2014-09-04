# -*- coding: utf-8 *-*

#foreign
import sys

#own
#from fancywidgets.dock import Dock
from fancytools.utils import StreamSignal
from PyQt4 import QtGui

#class MessageDock(Dock):


class Console(QtGui.QTextEdit):
	

	'''a simple qWidget with one read-only QTextEdit with a limited number of lines
	to display output generated with messages which 
	print() in black and raise() in red color'''

	def __init__(self, write_to_shell = False, *args, **kwargs):
		#NAME="Messages"
		MAXLINES = 300
		#size=sizeXY
		#area=None
		#widget=None
		#hideTitle=False
		#autoOrientation=False
		QtGui.QTextEdit.__init__(self, *args, **kwargs)#, area, size, widget, hideTitle, autoOrientation)

		self._red = QtGui.QColor(255,0,0)
		self._black = QtGui.QColor(0,0,0)
		
		#self._textEdit = QtGui.QTextEdit(self)
		self.setReadOnly(True)
		
		#self._cursor = self._textEdit.textCursor()
		self._format = QtGui.QTextCharFormat()
		
		# limit text length:
		self.document().setMaximumBlockCount(MAXLINES)
		
		#self.addWidget(self._textEdit)
		
		self._use_appbase_app = False
		try:
			# if the QApplication created through appbase.application
			# simply connect the the stream-output and -error signals
			self.session = QtGui.QApplication.instance().session
			self._use_appbase_app = True
			self.session.streamOut.message.connect(self.addTextOut)
			self.session.streamErr.message.connect(self.addTextErr)
		except AttributeError:
			# else create the StreamSignal object:
				# create 2 streamSignals for standard- and error-messages
			self.streamOut = StreamSignal()
			self.streamErr = StreamSignal()
			#connect those to different addText-methods
			self.streamOut.message.connect(self.addTextOut)
			self.streamErr.message.connect(self.addTextErr)
			# save the std output funcs:
			stdoutW = sys.stdout.write
			stderrW = sys.stderr.write
			# forward the std-signals to the new ones:
			sys.stdout = self.streamOut
			sys.stderr = self.streamErr
			if write_to_shell:
				self.streamOut.message.connect(stdoutW)
				self.streamErr.message.connect(stderrW)


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
		'''disconnect from stdout and stderr'''
		if self._use_appbase_app:
			self.session.streamOut.message.disconnect(self.addTextOut)
			self.session.streamErr.message.disconnect(self.addTextErr)
		else:
			# Restore sys.stdout and *err
			sys.stdout = sys.__stdout__
			sys.stderr = sys.__stderr__




if __name__ == '__main__':	
	import sys
	#from fancywidgets import DockArea
	app = QtGui.QApplication(sys.argv)
	#win = QtGui.QMainWindow()
	#area = DockArea()
	#win.setCentralWidget(area)
	
	d = Console(write_to_shell=True)

	#area.addDock(d)
	d.show()
	###############
	print (1,2,3,'test')
	def printError(evt):
		raise Exception('this is an error test')
	###############

	a = QtGui.QPushButton('press for error')
	a.clicked.connect(printError) 
	#d.addWidget(a)
	a.show()
	
	sys.exit(app.exec_())


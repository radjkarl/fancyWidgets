# -*- coding: utf-8 *-*

#foreign
import sys
from QtRec import QtCore
from QtRec import QtGui
QtGui = QtGui.origQtGui

from fancywidgets.dock import Dock
#from appBase.widgets.dock import Dock


class MessageDock(Dock):
	''''''

	def __init__(self, *args, **kwargs):
		NAME="Messages"
		MAXLINES = 300
		#size=sizeXY
		#area=None
		#widget=None
		#hideTitle=False
		#autoOrientation=False
		super(MessageDock, self).__init__(NAME, *args, **kwargs)#, area, size, widget, hideTitle, autoOrientation)
		self._red = QtGui.QColor(255,0,0)
		self._black = QtGui.QColor(0,0,0)
		self._textEdit = QtGui.QTextEdit(self)
		self._textEdit.setReadOnly(True)
		self._cursor = self._textEdit.textCursor()
		self._format = QtGui.QTextCharFormat()
		# limit textlength
		self._textEdit.document().setMaximumBlockCount(MAXLINES)
		self.addWidget(self._textEdit)
		#create 2 streamSignals for standart- and error-messages
		self.streamOut = StreamSignal()
		self.streamErr = StreamSignal()
		#self._logFile = session.log_file
		#connect those to different addText-methods
		self.streamOut.message.connect(self.addTextOut)
		self.streamErr.message.connect(self.addTextErr)
		#combine the system-stream-messages to the signals
		sys.stdout = self.streamOut
		sys.stderr = self.streamErr


	def addTextOut(self, text):
		self._currentColor = self._black
		self.addText(text)


	def addTextErr(self, text):
		self._currentColor = self._red
		self.addText(text)


	def addText(self, text):
		#move to the end of the doc
		self._textEdit.moveCursor(QtGui.QTextCursor.End)
		#set the textcolor
		self._format.setForeground(self._currentColor)
		#give the text-cursor the new format
		self._cursor.setCharFormat( self._format )
		#insert the text
		self._cursor.insertText(text)
		#log to file
		#print type(text)
		#self._logFile.write(unicode(text).encode('utf8'))
		#self._logFile.flush()
		

	def __del__(self):
		# Restore sys.stdout and *err
		sys.stdout = sys.__stdout__
		sys.stderr = sys.__stderr__



class StreamSignal(QtCore.QObject):
	message = QtCore.Signal(str)
	def __init__(self, logFile=None, parent=None):
		super(StreamSignal, self).__init__(parent)

	def write(self, message):
		self.message.emit(message)


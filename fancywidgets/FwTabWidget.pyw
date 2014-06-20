# -*- coding: utf-8 -*-
from PyQt4 import QtGui

class FwTabWidget(QtGui.QTabWidget):
	'''
	xxxxxxxxxxxx
	'''
	#def __init__(self):
	#	super(Tab, self).__init__()
	def __iter__(self):
		self._i = -1
		return self
	
	def next(self):
		self._i += 1
		if self._i == self.count():
			raise StopIteration()
		return self.widget(self._i)
		
		
	def removeTab(self, tab):
		'''allows to remove a tabirectly -not only by giving its index'''
		if type(tab) != int:
			tab = self.indexOf(tab)
		return super(FwTabWidget, self).removeTab(tab)

	def tabText(self,tab):
		if type(tab) != int:
			tab = self.indexOf(tab)
		return super(FwTabWidget, self).tabText(tab)

if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	w= FwTabWidget()
	t1 = QtGui.QLabel(FwTabWidget.__doc__)	
	t2 = QtGui.QWidget()
	w.addTab(t1,'one')
	w.addTab(t2,'two')
	w.show()
	sys.exit(app.exec_())

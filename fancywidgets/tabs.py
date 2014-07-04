# -*- coding: utf-8 -*-
from QtRec import QtGui

class Tabs(QtGui.QTabWidget):
	
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
		return super(Tabs, self).removeTab(tab)

	def tabText(self,tab):
		if type(tab) != int:
			tab = self.indexOf(tab)
		return super(Tabs, self).tabText(tab)

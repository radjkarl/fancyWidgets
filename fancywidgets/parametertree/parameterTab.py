# -*- coding: utf-8 *-*

#own
from nIOp.parametertree import ParameterTree


class ParameterTab(ParameterTree):
	'''
	the preference tab that belongs to each Display
	'''

	def __init__(self, parameter):
		ParameterTree.__init__(self, showHeader=False)
		#self.name = name
		self.setAnimated(True)
		if parameter:
			self.setParameters(parameter, showTop=False)

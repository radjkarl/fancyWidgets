# -*- coding: utf-8 -*-

#own
from appBase.structure import Structure
from appBase.signalList import Signal

from Parameter import Parameter
from time import gmtime, strftime

_string_types = ['str','unicode','QString']


class ParameterContainer(Structure):

	def __init__(self, parent):
		Structure.__init__(self,parent)
		self._logList = []

		self.sigParamChanged = Signal()

		param = self.createParam()
		self.pUndo = param.addChild({
			'name':'Undo',
			'type':'action',
			'setValue':self.undo})
		self.pRedo = param.addChild({
			'name':'Reddo',
			'type':'action',
			'setValue':self.redo})
		self.pSaveHistory = param.addChild({
			'name':'Save History',
			'type':'bool',
			'value':False})
		self.pSaveTimeStamp = param.addChild({#TODO: rAUS
			'name':'Save Timestamp',
			'type':'bool',
			'value':True})


	def undo(self):
		pass
	def redo(self):
		pass


	#TODO: wer erstellt und verwaltet jetzt am besten die param???
	def add(self, owner, argDict={}):
		if 'name' not in argDict:
			argDict['name'] = owner.name
		if 'type' not in argDict:
			argDict['type'] = 'group'
	#	argDict['master'] = owner
		p = Parameter.create(self, **argDict)
		return p


	def logMethod(self, method, value=''):
		param = method.im_self
		param._log_pos = len(self._loglist)
		timestamp = strftime("%d.%m.%Y|%H:%M:%S", gmtime())
		self._loglist.append( (method, value, timestamp ) )


	def _legalizeValue(self, value):
		if type(value).__name__ in _string_types: #is string?
			#replace inner-string-signs
			value = value.replace("'","<str>")
			if '\n' in value: #create a multilinestring
				value = "'''%s'''"%value
			else:
				value = "'%s'"%value
		else:
			value = str(value)
		return value


	def _resetLogName(self, inst):
		inst._log_name = False


	def save(self):
		logName = '__main__.py'
		logFolder = ''
		logContent =''# open(logFileName, 'w')
		nameDict = {}
		#reset all earlier given param param names:
		self.session.forAll(self._resetLogName,self.session)

		logContent += '''#!/usr/bin/env python
	# -*- coding: utf-8 *-*
	
	# this file stores all method-calls though the preference-tabs
	# of the Gui. Though this procedure all entries of the are stores chonologically
	# This allous you to reload the whole case or to use is for following indiviual
	# problems even without using the Gui
	
	from nIOp import Session
	session = Session()
	
	# The following calls were generated while using the Gui:
	
	'''
		#for all logged methods:
		for n,(method, value, timeName) in enumerate(self._loglist):
			param = method.im_self
			if not param.removed and (self.pSaveHistory.value or param._log_pos == n):
				#do log:
				value = self._legalizeValue(value)
				#format time-string if wanted
				if self.pSaveTimeStamp.value:
					timeName = ",\n\ttime='%s'" %timeName
				else:
					timeName = ''
				#if param only one time used
				if param.getLastLogPos() == n:
					(master, paramPath) = param.path()
					structurePath = master.path(param)
					#get param and exec. its method directly
					logContent += "session.%s.param('%s').%s('%s'%s)\n" %(
						structurePath,
						str(paramPath[1:-1]),method.__name__, value, timeName)
				#else param is used multiple times - therefore it is usefull to give him a name:
				else:
					if not param._log_name:
						#no name given jet
						(master, paramPath) = param.path()
						structurePath = master.path(param)
						paramName = ''
						for p in paramPath:
							paramName += p[:4]
						n = nameDict[paramName]
						if not n:#paramName not used so far
							nameDict[paramPath] = 1
						else:#append ParamName with individual number
							n += 1
							nameDict[paramName] = n
							paramName += str(n)
						#name the param:
						logContent += "%s = session.%s.param('%s')\n" %(
							paramName, structurePath, str(paramPath)[1:-1])
						#let the param know its name
						param._log_name = paramName
					logContent += "%s%s.%s('%s'%s)\n" %(paramName,method.__name__, value, timeName)
		logContent += '\n\nsession.restore()'
		logContent += '\nsession.gui.show()'

		#logFile.close()
		print "startscript: %s written" %logName
		return [(logName,logFolder, logContent)]
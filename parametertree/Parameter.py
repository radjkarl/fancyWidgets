# -*- coding: utf-8 -*-


import nIOp
from appBase.signalList import Signal

#origParameter = Parameter
from pyqtgraph.parametertree.Parameter import Parameter as origParameter
from pyqtgraph.parametertree.Parameter import registerParameterType

from pyqtgraph.parametertree.Parameter import PARAM_TYPES, PARAM_NAMES


from pyqtgraph import asUnicode
from pyqtgraph.Qt import QtGui, QtCore

import traceback


class Parameter(origParameter):
	'''
	add new options to pyQtGraphs 'Parameter'-Class ot be fully interactive
	and log all changes:
		* 'setValue'
		* 'getValue'
		* 'setLimits'
		* 'remove'
		* 'duplicatable'
		* 'index'
		* 'init'
		* 'static' ...dont update other params when param change
		* 'key' - for shortcuts (coded in parameterItem - because its gui-dependent)
		* 'log' ...
		* 'isGroup' True/False
		* 'icon' -> 'path/to/icon' based on the nIOp-dir
	'''
	@staticmethod
	def create(container, **opts):
		#NEW#
		typ = opts.get('type', None)
		if typ is None:
			raise Exception("needed key 'type' not in given %s" %opts)
		try:
			opts['name'] = opts['getName']()
		except:
			pass
		try:
			l = opts['getLimits'] ()
			if isinstance(l,list):
				opts['limits'] = l
		except KeyError:
			pass

		if 'value' not in opts:
			try:
				opts['value'] = opts['getValue'] (opts['index'])
				#print 333
			except (KeyError, TypeError):
				#index not in list or getMethod doesnt take index
				#print 66, opts['name'], opts.get('index')
				try:
					opts['value'] = opts['getValue'] ()
				except KeyError:
					pass

		cls = PARAM_TYPES[opts['type']]
		return cls(container, **opts)


	def __init__(self, container, **opts):
		self.container = container
		self.session = self.container.session
		try:
			if self.session.debug_mode:
				self._execMethod = self._execMethodDebugMode
			else:
				self._execMethod = self._execMethodNormal
			if self.opts.get('key'):
				self.session.gui.sigCreated.connect(self._addKey)
		except:#parent not valid
			self._execMethod = self._execMethodNormal

		self._exist = False
		origParameter.__init__(self, **opts)
		self._exist = True
		self._key = None
		self._blocked_setValue = False
		self._inBatch = False
		self._is_child = False
		self._removed = False
		self.sigDuplicated = Signal()


	def init(self):
		self.setValue(value=self.value, blockSignal=self._logValue)
		return self



	def _addKey(self):
		key = self.opts.get('key',None)
		setValue = self.opts.get('setValue',None)
		k = QtGui.QShortcut(self.session.gui)
		if not isinstance(key, QtGui.QKeySequence):
			key = QtGui.QKeySequence(key)
		k.setKey(QtGui.QKeySequence(key))
		self.session.gui.shortcuts[key.toString()] = self
		k.setContext(QtCore.Qt.ApplicationShortcut)
		k.activated.connect(setValue)
		self._key = k


	def block(self):
		self.blockSignals(True)
		if self._key:
			self._key.blockSignals(True)


	def unblock(self):
		self.blockSignals(False)
		if self._key:
			self._key.blockSignals(False)


	def show(self, s=True):
		if s:
			self.update(force=True)
		origParameter.show(self,s)


	def remove(self, log=True, **kwargs):
		if log:
			self.container.logMethod(self, self.remove, **kwargs)
		self._remove()


	def _remove(self):
		try:
			m = self.opts['setRemove']
			index = self.opts.get('index', None)
			try:
				m(index, self)
			except TypeError:
				try:
					m(self)
				except TypeError:
					m () #remove-method doesn't take anything
		except KeyError:
			pass
		self.forAllParamRecursive(self,self._checkForBatch)
		self.forAllParamRecursive(self,self._setRemoved)
		super(Parameter, self).remove()
		self.session.container.sigParamChanged.emit()


	def _setRemoved(self):
		self.removed = True


	def forAllParamRecursive(self,param, method):
		for ch in param.children():
			self.forAllParamRecursive(ch, method)
		method(param)


	def _checkForBatch(self,param):
		if param._inBatch:
			nIOp.getBatch().removeParam(param.pathToMaster)


	def _logValue(self):
		#TODO: kick self.value() != "-" ??
	#	print self.name()
		value = self.value()
		if value != "-" and not self._blocked_setValue:
			if self.opts.get('log') != False:
				self.container.logMethod(self.setValue, value)
			self.setValue(value)


	@property
	def limits(self):
		return self.opts['limits']

	@limits.setter
	def _setLimits(self, l):
		self.setOpts(limits=l)


	def setName(self,name, log=True):
		name =  super(Parameter,self).setName(asUnicode(name))
		if self._exist and self._is_child:
			if self.opts['renamable'] and log:
				self.container.logMethod(self.setName,name)
		return name


	def path(self):
		p = self.parent()
		l = [self.name()]
		while p:
			l.insert(0,p.name())
			c = p
			p = p.parent()
		return c.opts['master'], l




	def _execMethodDebugMode(self, value, pmethod):
		index = self.opts.get('index', None)
		if index != None:
			try:
				return pmethod(value, index)
			except TypeError:
				print traceback.print_exc()
				return None
		try:
			return pmethod(value)
		except TypeError:
			print traceback.print_exc()
			return pmethod()


	def _execMethodNormal(self, value, pmethod):
		print value, pmethod
		index = self.opts.get('index', None)
		if index != None:
			try:
				return pmethod(value, index)
			except TypeError:
				return None
		try:
			return pmethod(value)
		except TypeError:
			try:
				return pmethod()
			except TypeError:
				print traceback.print_exc()

#	@property
#	def value(self):
#		return super(Parameter, self).value()
#TODO: warum klappt dasnicht???
#	@value.setter
	def setValue(self, value, blockSignal=None):
		if type(value) == str:
			value = asUnicode(value)
		pmethod = self.opts.get('setValue', None)
		if pmethod:
			self._execMethod(value, pmethod)
		return super(Parameter, self).setValue(value, blockSignal)


	#def logMethod(self, value, method=None):
		#if not method:
			#method = self._master.setParam
		#self.container.logMethod(method, value)


	def addToBatch(self, **kwargs):
		self._inBatch = True
		self.container.logMethod(self.addToBatch, **kwargs)
		#self.container.logMethod(self._master.addParamToBatch, **kwargs)
		self.session.batch.addParam(self, **kwargs)

	def hasVisibleChilds(self):
		for ch in self.children():
			if ch.opts['visible']:
				return True
		return False


	def moveChild(self, child, index, log=True):
		if log:
			self.container.logMethod(self._master.moveParam,child.name(),index)
		self.removeChild(child)
		self.insertChild(index,child)


	def duplicate(self, log=True):
		if log:
			self.container.logMethod(self.duplicate)
		self.sigDuplicated.emit()
	#	out = self._master.duplicateChild()
	#	return out


	def expand(self, boolean, log=True, **kwargs):
		if boolean != self.opts['expanded']:
			if log:
				self.container.logMethod(self.expand,
					boolean, **kwargs)
			self.setOpts(expanded=boolean)


	#def _removeListEntry(self, entry):
		#try:
			#l = self.opts['limits']
			#i = l.index(entry)
			#l.pop(i)
			#self.sigLimitsChanged.emit(self, l)
		#except (KeyError, ValueError):
			#pass


	def isVisible(self):
		if self.opts['visible']:
			p = self
			while True:
				p = p.parent()
				if not p:
					return True
				if not p.opts['visible']:
					break
		return False


	def setValues(self, masterParam):
		'''duplicate values, names and limits from one analoque parameter recursively'''
		self.setValue(masterParam.value())
		try:
			self.setLimits(masterParam.opts['limits'])
		except KeyError:
			pass
		self.setName(masterParam.name(), log=False)

		for myChild,masterChild in zip(self.children(),masterParam.children()):
			myChild.setValues(masterChild)


	def replaceWith(self, param):
		'''replace this parmeter with another'''
		i = self.parent().children().index(self)
		#TODO: transfer the children:
		p = self.parent()
		self.parent().removeChild(self)
		p.insertChild(i, param)
		self = param
		#return p.insertChild(i, param)


	def update(self, force=False):
		if not force and not self.isVisible():
			return
		try:
			self.setName(self.opts['getName'](), log=False)
		except KeyError:
			pass
		try:
			l = self.opts['getLimits'] ()
			if isinstance(l,list):#if is valid
				self.setLimits( l )
		except KeyError:
			pass
		try:
			self.setValue(self.opts['getValue'] (self.opts['index']))
		except (KeyError, TypeError):
			#index not in list or getMethod doesnt take index
			try:
				self.setValue( self.opts['getValue']())
			except KeyError:
				pass


	def insertChild(self,pos, child):
		"""
		Insert a new child at pos.
		If pos is a Parameter, then insert at the position of that Parameter.
		If child is a dict, then a parameter is constructed using
		:func:`Parameter.create <pyqtgraph.parametertree.Parameter.create>`.
		"""
		if isinstance(child, dict):
			child = Parameter.create(self.container, **child)
		
		name = child.name()
		if name in self.names and child is not self.names[name]:
			#changed##
			#if child.opts.get('autoIncrementName', False):
			name = self.incrementName(name)
			child.setName(name, log=False)
			#else:
			#	raise Exception("Already have child named %s" % str(name))
		####new#####
		if pos < 0:
			pos = len(self.childs)-1+pos
		#####old#####
		if isinstance(pos, Parameter):
			pos = self.childs.index(pos)
			
		with self.treeChangeBlocker():
			if child.parent() is not None:
				child.remove()
				
			self.names[name] = child
			self.childs.insert(pos, child)
			child.parentChanged(self)
			self.sigChildAdded.emit(self, child, pos)
			child.sigTreeStateChanged.connect(self.treeStateChanged)
			####new####
			x = child.sigValueChanged
			if child.isType('action'):
				x = child.sigActivated

			x.connect(child._logValue)
			if not child.opts.get('static', False):
				x.connect(self.container.sigParamChanged.emit)
				#also update when name change:
				child.sigNameChanged.connect(self.container.sigParamChanged.emit)

			#child.findMaster()

			activeWith = ['getValue', 'getLimits', 'getName']
			isActive = bool([i for i in activeWith if child.opts.get(i)])
			
			if isActive:
				self.container.sigParamChanged.connect(child)
		child._is_child = True
		return child





	#to enable easy manipulation of the parameter:
	#attr = property(origParameter.value,_setValueViaCode,_remove)





	##TODO: brauchich den wirklich?
	#def makeProperty(self, inst):
		## set a property for the given instance dynamically with access to
		## the get, set and del-method of this class
		#name = utils.legalizeFilename(self.name())
		#inst.__setattr__('_get_'+name,self.value)
		#inst.__setattr__('_set_'+name,self._setValueViaCode)
		#inst.__setattr__('_del_'+name,self._remove)
		#return property(
			#lambda self: self.__getattribute__('_get_'+name)(),
			#lambda self,val: self.__getattribute__('_set_'+name)(val),
			#lambda self: self.__getattribute__('_del_'+name)() )
##TODO: evtl. is folgendes schneller für priority
#class HackedProperty(object):
    #def __init__(self, f):
        #self.f = f
    #def __get__(self, inst, owner):
        #return getattr(inst, self.f.__name__)()

#class Foo(object):
    #def _get_age(self):
        #return 11
    #age = HackedProperty(_get_age)

#class Bar(Foo):
    #def _get_age(self):
        #return 44

#print Bar().age
#print Foo().age
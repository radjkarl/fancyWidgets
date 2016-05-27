# -*- coding: utf-8 -*-

from fancytools.os.PathStr import PathStr

#foreign
from PyQt4 import QtGui


class Dialogs(object):
    '''
    * saves the last path to save and open a file/directory
    '''
    def __init__(self, dirname=None):
        self.opts = {'save': dirname, 'open': dirname}


    def saveState(self):
        '''
        save options to file 'dialogs.conf'
        '''
#         p = PathStr(path).join('dialogs.conf')
#         with open(p, 'w') as f:
#             f.write(str(self.opts))
        return self.opts


    def restoreState(self, state):
        '''
        restore options from file 'dialogs.conf'
        '''
#         p = PathStr(path).join('dialogs.conf')
#         with open(p, 'r') as f:
        self.opts.update(state)


    def getSaveFileName(self, *args, **kwargs):
        '''
        analog to QtGui.QFileDialog.getSaveFileNameAndFilter
        but returns the filename + chosen file ending even if not typed in gui
        '''
        if not 'directory' in kwargs:
            if self.opts['save']:
                if self.opts['save']:
                    kwargs['directory'] = self.opts['save']
            
        fname = QtGui.QFileDialog.getSaveFileName(**kwargs)
        if fname:
            p = PathStr(fname)
            self.opts['save'] = p.dirname()
            if self.opts['open'] is None:
                self.opts['open'] = self.opts['save']
            return p           
    
    
    def _processOpenKwargs(self, kwargs):
        if not kwargs.get('directory'):
            if self.opts['open']:
                kwargs['directory'] = self.opts['open']    
        return kwargs


    def getOpenFileName(self, **kwargs):
        kwargs = self._processOpenKwargs(kwargs)
        fname = QtGui.QFileDialog.getOpenFileName(**kwargs)
        if fname:
            p = PathStr(fname)
            self.opts['open'] = p.dirname()
            return p


    def getOpenFileNames(self, **kwargs):
        kwargs = self._processOpenKwargs(kwargs)
        fnames = list(QtGui.QFileDialog.getOpenFileNames(**kwargs))
        for n,f in enumerate(fnames):
            fnames[n] = PathStr(f)
        if fnames:
            self.opts['open'] = PathStr(f).dirname()
        return fnames
  
    
    def getExistingDirectory(self, **kwargs):
        kwargs = self._processOpenKwargs(kwargs)
        fname = QtGui.QFileDialog.getExistingDirectory(**kwargs)
        if fname:
            p = PathStr(fname)
            self.opts['open'] = p.dirname()
            return p

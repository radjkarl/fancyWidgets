# -*- coding: utf-8 -*-

from fancytools.os.PathStr import PathStr

#foreign
from PyQt4 import QtGui


class Dialogs(object):
    '''
    * saves the last path to save and open a file/directory
    
    '''
    
    def __init__(self):
        self.last_save_dir = None
        self.last_open_dir = None


    def _processKwargs(self, kwargs):
        if 'caption' not in kwargs:
            kwargs['caption'] = 'Save File'
            
        if not kwargs.get('directory') and self.last_save_dir:
            kwargs['directory'] = self.last_save_dir
        return kwargs


    def _processOutput(self, fname, ffilter):
        fname = unicode(fname)
        ffilter = unicode(ffilter)
        if  '.' not in fname:
            i = ffilter.index('*')+1
            for o,z in enumerate(ffilter[i:]):
                if z in (' ', ')'):
                    break
            ffilter = ffilter[i:o+i]
            fname = fname + ffilter
        
        p = PathStr(fname)
        if p:
            self.last_open_dir = p.dirname()  
        return p



    def getSaveFileName(self, **kwargs):
        '''
        analog to QtGui.QFileDialog.getSaveFileNameAndFilter
        but returns the filename + chosen file ending even if not typed in gui
        '''
        kwargs = self._processKwargs(kwargs)
        if kwargs and 'filter' in kwargs:
            (fname,ffilter) = QtGui.QFileDialog.getSaveFileNameAndFilter(**kwargs)
            return self._processOutput(fname, ffilter)
        else:
            fname = QtGui.QFileDialog.getSaveFileName(**kwargs)
            p = PathStr(fname)
            if p:
                self.last_open_dir = p.dirname()
                return p           
    
    
    def getOpenFileName(self, **kwargs):
        kwargs = self._processKwargs(kwargs)
        fname = QtGui.QFileDialog.getOpenFileName(**kwargs)
        p = PathStr(fname)
        if p:
            self.last_open_dir = p.dirname()
        return p


    def getOpenFileNames(self, **kwargs):
        kwargs = self._processKwargs(kwargs)
        fnames = QtGui.QFileDialog.getOpenFileNames(**kwargs)
        for n,f in enumerate(fnames):
            fnames[n] = PathStr(f)
        if f:
            self.last_open_dir = PathStr(f).dirname()
        return fnames
  
    
    def getExistingDirectory(self, **kwargs):
        if not kwargs.get('directory') and self.last_open_dir:
            kwargs['directory'] = self.last_open_dir
        #kwargs = _checkDir(kwargs)
        if 'caption' not in kwargs:
            kwargs['caption'] = 'Open Folder'
        fname = QtGui.QFileDialog.getExistingDirectory(**kwargs)
        #this [f***ing] bug occurs only on windows
        #if type(fname) == tuple:
        #    fname = fname[0]
        p = PathStr(fname)
        if p:
            self.last_open_dir = p.dirname()
        return p

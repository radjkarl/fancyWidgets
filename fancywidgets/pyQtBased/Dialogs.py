# -*- coding: utf-8 -*-

from fancytools.os.PathStr import PathStr

# foreign
from qtpy import QtGui, QtPrintSupport, QtWidgets


class Dialogs(object):
    """
    * saves the last path to save and open a file/directory
    """

    def __init__(self, dirname=None):
        self.opts = {'save': dirname, 'open': dirname}

    def saveState(self):
        """
        save options to file 'dialogs.conf'
        """
#         p = PathStr(path).join('dialogs.conf')
#         with open(p, 'w') as f:
#             f.write(str(self.opts))
        return self.opts

    def restoreState(self, state):
        """
        restore options from file 'dialogs.conf'
        """
#         p = PathStr(path).join('dialogs.conf')
#         with open(p, 'r') as f:
        self.opts.update(state)

    def getSaveFileName(self, *args, **kwargs):
        """
        analogue to QtWidgets.QFileDialog.getSaveFileNameAndFilter
        but returns the filename + chosen file ending even if not typed in gui
        """
        if 'directory' not in kwargs:
            if self.opts['save']:
                if self.opts['save']:
                    kwargs['directory'] = self.opts['save']
        fname = QtWidgets.QFileDialog.getSaveFileName(**kwargs)
        if fname:
            if type(fname) == tuple:
                #only happened since qt5
                #getSaveFileName returns (path, ftype)
                if not fname[0]:
                    return
                p = PathStr(fname[0])
                if not p.filetype():
                    ftyp = self._extractFtype(fname[1]) 
                    p = p.setFiletype(ftyp)
            else:
                p = PathStr(fname)
            self.opts['save'] = p.dirname()
            if self.opts['open'] is None:
                self.opts['open'] = self.opts['save']
            return p

    @staticmethod
    def _extractFtype(ftypestr):
        # extracts pbm from e.g. 'Portable image format (*.pbm *.pgm *.ppm)'
        i0 = ftypestr.index('*')
        for i1, d in enumerate(ftypestr[i0+1:]):
            if not d.isalpha():
                break
        i1 += 1+i0
        return ftypestr[i0,i1]
        
        

    def _processOpenKwargs(self, kwargs):
        if not kwargs.get('directory'):
            if self.opts['open']:
                kwargs['directory'] = self.opts['open']
        return kwargs

    def getOpenFileName(self, **kwargs):
        kwargs = self._processOpenKwargs(kwargs)
        fname = QtWidgets.QFileDialog.getOpenFileName(**kwargs)
        if isinstance(fname, tuple):
            fname = fname[0]
        if fname:
            p = PathStr(fname)
            self.opts['open'] = p.dirname()
            return p

    def getOpenFileNames(self, **kwargs):
        kwargs = self._processOpenKwargs(kwargs)
        fnames = QtWidgets.QFileDialog.getOpenFileNames(**kwargs)
        # PyQt4 and 5 comp. workaround
        if isinstance(fnames, tuple) and isinstance(fnames[0], list):
            fnames = fnames[0]
        for n, f in enumerate(fnames):
            fnames[n] = PathStr(f)
        if fnames:
            self.opts['open'] = PathStr(f).dirname()
        return fnames

    def getExistingDirectory(self, **kwargs):
        kwargs = self._processOpenKwargs(kwargs)
        fname = QtWidgets.QFileDialog.getExistingDirectory(**kwargs)
        if fname:
            p = PathStr(fname)
            self.opts['open'] = p.dirname()
            return p

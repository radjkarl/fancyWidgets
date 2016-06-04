from PyQt4 import QtGui, QtCore
import __builtin__
import importlib
from pkginfo import Installed
import warnings
# OWN
from fancywidgets.pyQtBased.highlighter import Highlighter
from fancytools.fcollections.naturalSorting import naturalSorting

# FIXME
# in order to also have in in a frozen environment
# see _getInstalledModules
import _installed_modules


class CodeEditor(QtGui.QWidget):
    '''
    A simple code editor with a QPlainTextEdit and line numbers of the left side
    '''
    def __init__(self, dialog=None):
        QtGui.QWidget.__init__(self)

        if dialog is None:
            dialog = QtGui.QFileDialog
        self.dialog = dialog

        self.editor = _CodeTextEdit(self)
        self.lineNumbers = _LineNumberArea(self.editor)

        l = QtGui.QHBoxLayout()
        self.setLayout(l)
        l.addWidget(self.lineNumbers)
        l.addWidget(self.editor)

    def addGlobals(self, g):
        '''
        g ==> {name:description,...}
        '''
        self.editor._globals.update(g)
        pass



class _CodeTextEdit(QtGui.QPlainTextEdit):
    '''
    a text editor with ... 
    * monospace font, 
    * tab2spaces, 
    * python syntax highlighter
    * 'save to file' in context menu 
    '''
    def __init__(self, codeEditor):
        QtGui.QPlainTextEdit.__init__(self)

        self._globals = {}
        self._mg = None
        self.codeEditor = codeEditor
        # FONT: set monospace
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setStyleHint(QtGui.QFont.Monospace)
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)
        # TAB to spaces
        tabStop = 4  # 4 characters
        metrics = QtGui.QFontMetrics(font)
        self.setTabStopWidth(tabStop * metrics.width(' '))
        # SCROLL BAR - horizontal:
        self.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        # SYNTAX highlighter:
        self.highlighter = Highlighter(self.document(), "python")


    @staticmethod
    def _nameFromModName(name):
        #mod name is given as 'mon (v0.1)'
        #return 'mod'
        return name[:name.index(' ')]


    def _addImportModule(self, name):
        #insert 'import <mod>' at the begin
        name = self._nameFromModName(name)

        c = self.textCursor()
        p = c.position()
        c.setPosition(0)
        self.setTextCursor(c)
        self.insertPlainText('import %s\n' %name)
        c.setPosition(p)
        self.setTextCursor(c)
        self.moveCursor(QtGui.QTextCursor.Down)


    def _addObject(self, name):
        cc = QtGui.QTextCursor
        c = self.textCursor()
        c.select(cc.WordUnderCursor)
        txt = c.selectedText()
        if txt:
            c.movePosition(cc.EndOfWord)
            self.setTextCursor(c)
            if c.hasSelection():
                c.removeSelectedText()
                txt = txt + ' '
            else:
                txt = ' '
        c.clearSelection()

        try:
            if callable(eval(name)):
                txt += name + '()'
            else:
                txt += name
        except (NameError, SyntaxError):
            txt += name

        self.insertPlainText(txt)


    def _addMenuEntries(self, menu, entries, fn):
        #limit number of entries to be shown in a menu
        #create sub menus (e.g. 'A-F') 

        entries = sorted(entries)

        def getLetter():
            try:
                return entries[i+mx][0].capitalize()
            except IndexError:
                return entries[-1][0].capitalize()
        c = -1
        i = 0
        mx = 15
        if len(entries) < mx:
            sub = menu
        else:
            letter = getLetter()
            sub = menu.addMenu('%s-%s'
                               % (entries[0][0].capitalize(),letter) )
        for e in entries:
            sub.addAction(e).triggered.connect(
                lambda checked, n=e: fn(n))
            c += 1
            i += 1
            if c == mx:
                new_letter = getLetter()
                sub = menu.addMenu(letter + '-' + new_letter)
                letter = new_letter
                c = 0


    def _buildGlobalsMenu(self):

        mg = self._mg
        mg.aboutToShow.disconnect(self._buildGlobalsMenu)

        # GIVEN GLOBALS:
        for gi in naturalSorting(self._globals.keys()):
            mg.addAction(gi).triggered.connect(
                lambda checked, n=gi: self._addObject(n))
        if self._globals:
            mg.addSeparator()

        # BUILT-INs
        mb = mg.addMenu('Built-in Objects')
        l = [i for i in dir(__builtin__)]
        # exclude warnings and errors:
        err = []
        war = []
        for i in xrange(len(l)-1,-1,-1):
            v = l[i]
            if v.endswith('Error') or v.endswith('Exception'):
                err.append(l.pop(i))
            elif v.endswith('Warning'):
                war.append(l.pop(i))

        self._addMenuEntries(mb, l, self._addObject)
        m = mb.addMenu('Errors')
        self._addMenuEntries(m, err, self._addObject)

        m = mb.addMenu('Warnings')
        self._addMenuEntries(m, war, self._addObject)
        # MODULES
        mm = mg.addMenu('Installed modules')

        self._addMenuEntries(mm, self._getInstalledModules(), 
                             self._addImportModule)


    def _getInstalledModules(self):
        try:
            pip = importlib.import_module('pip')#save some startup time
            l = sorted(
                    ["%s (%s)" % (i.key, i.version) 
                     for i in pip.get_installed_distributions()]
                       )
        except ImportError:
            #pip doesn't exist
            l = None
        #FIXME: with pip v8.1.1. l will be []
        #if executed in a frozen environment
        #for this case load infos from file:
        if not l:
            l = _installed_modules.l 
        else:
            #update file
            with open(_installed_modules.__file__, 'w') as f:
                f.write('''#this file is auto generated by 
#CodeEditor.py - do not delete it
l=''')
                f.write(str(l))
        return l
            
            
    def _globalMenuHovered(self, action):
        #show a functions/modules __doc__ as tooltip
        mg = self._mg
        s = str(action.text())
        txt = None
        try:
            txt = eval(s).__doc__

        except (NameError, SyntaxError):
            #action text is not a global
            #maybe because its just menu text
            #or if will be become global, when code txt is compiled: 
            
            if s in self._globals:
                txt = self._globals[s]
            #in case a module is hovered:
            elif '(' in s:
                
                s = self._nameFromModName(s)
                with warnings.catch_warnings():
                    #ignore-> UserWarning: No PKG-INFO found for package: ...
                    warnings.simplefilter("ignore")
                    #FIXME: txt will be empty if executed in frozen environment:
                    txt = Installed(s).description
        
        if txt is None:
            txt = ''
            
        elif len(txt)>1000:
            txt = txt[:1000]
            txt += '\n...'
            
        QtGui.QToolTip.showText(
            QtGui.QCursor.pos(), txt,
            mg, mg.actionGeometry(action))


    def getGlobalsMenu(self):
        if self._mg is not None:
            return self._mg
        
        #add globals to menu:
        self._mg = mg = QtGui.QMenu('Globals')
        #to show tooltips of its containing actions:
        mg.hovered.connect(self._globalMenuHovered)
        #make font bold:
        mga = mg.menuAction() 
        f = mga.font()
        f.setBold(True)    
        mga.setFont(f)
        #only build, when needed:
        mg.aboutToShow.connect(self._buildGlobalsMenu)
        # mg.aboutToHide.connect(mg.clear) #this doesnt free memory,so leave it 
        return mg
          

    def contextMenuEvent(self, event):
        '''
        Add menu action:
        * 'Show line numbers'
        * 'Save to file'
        '''
        menu = QtGui.QPlainTextEdit.createStandardContextMenu(self)
        mg = self.getGlobalsMenu()
        
        a0 = menu.actions()[0]
        menu.insertMenu(a0, mg)
        menu.insertSeparator(a0)

        menu.addSeparator()
        a = QtGui.QAction('Show line numbers', menu)
        l = self.codeEditor.lineNumbers
        a.setCheckable(True)
        a.setChecked(l.isVisible())
        a.triggered.connect(lambda checked: l.show() if checked else l.hide())
        menu.addAction(a)

        menu.addSeparator()
        a = QtGui.QAction('Save to file', menu)
        a.triggered.connect(self.saveToFile)
        menu.addAction(a)

        menu.exec_(event.globalPos())


    def saveToFile(self):
        '''
        Save the current text to file
        '''
        filename = self.codeEditor.dialog.getSaveFileName()
        if filename and filename != '.':
            with open(filename, 'w') as f:
                f.write(self.toPlainText())
            print('saved script under %s' %filename) 


    def toPlainText(self):
        '''
        replace [tab] with 4 spaces 
        '''
        txt = QtGui.QPlainTextEdit.toPlainText(self)
        return txt.replace('\t', '    ')



class  _LineNumberArea(QtGui.QPlainTextEdit):
    '''
    Left area to show line numbers of the code editor
    '''
    def __init__(self, editor):
        QtGui.QPlainTextEdit.__init__(self)
        self.setReadOnly(True)
        self.setFont(editor.font())
        self.setEnabled(False)
        self.setFixedWidth(35)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setFrameStyle(0)
        self.appendPlainText(str(1))

        editor.blockCountChanged.connect(self._updateNumbers)  
        editor.verticalScrollBar().sliderMoved.connect(self._syncHScrollBar)


    def _syncHScrollBar(self, val):
        '''
        Synchronize the view with the code editor
        '''
        self.verticalScrollBar().setValue(val)


    def _updateNumbers(self, linenumers):
        '''
        add/remove line numbers
        '''
        b = self.blockCount()
        c = b - linenumers
        if c > 0:
            # remove lines numbers
            for _ in range(c):
                # remove last line:
                self.setFocus()
                storeCursorPos = self.textCursor()
                self.moveCursor(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
                self.moveCursor(QtGui.QTextCursor.StartOfLine, QtGui.QTextCursor.MoveAnchor)
                self.moveCursor(QtGui.QTextCursor.End, QtGui.QTextCursor.KeepAnchor)
                self.textCursor().removeSelectedText()
                self.textCursor().deletePreviousChar()
                self.setTextCursor(storeCursorPos)
        elif c < 0:
            # add line numbers
            for i in range(-c):
                self.appendPlainText(str(b+i+1))



if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    w = CodeEditor()
    w.setWindowTitle(w.__class__.__name__)
    w.editor.setPlainText('#python highlighting\ni = int(5)\ndef fn(a,i):\n\tprint a,i')
    w.show()
    app.exec_()

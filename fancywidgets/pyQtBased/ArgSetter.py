from PyQt4 import QtGui, QtCore



class ArgSetter(QtGui.QDialog):
    '''Create an window to setup attributes graphically

    useful as quick configurator for other functions/classes that need 
    keyword arguments that must be passed graphically 
    e.g. for py2exe/pyinstaller apps
    '''
    validators = {float: QtGui.QDoubleValidator, 
                  int: QtGui.QIntValidator}

    def __init__(self, title, argdict, stayOpen=False, saveLoadButton=False,
                 savePath='config.txt', loadPath='config.txt', 
                 introduction=None, unpackDict=False):
        '''
        ====================   =========================================================
        Argument               Comment
        ====================   =========================================================
        title                  title of the window
        argdict                a dict of all arguments to set up:
                               e.g. {'arg1: {'value':1, 'limits':range(0,10)}, ...}
                               valid keywords are:
                                   'value' -> the value of the argument
                                   'limits' -> [list, tuple] if only specific values are valid
                                   'unit' -> show a unit after the value
                                   'tip' -> show a tool-tip
                                   'dtype' -> the data-type of the value
                                              * int, str, float, bool
                                              * file, dir  -> for selecting a file or folder
                                              * line  -> to add a horizontal separation line
                               for ordered entries use OrderedDict
        stayOpen                   True -> dialog stays open after it is finished
                               useful if values should still be changeable
        saveLoadButton         True -> add 2 buttons to save and load these preferences
        savePath               Default save path
        loadPath               Default load path
        unpackDict             True, False | True: 
        ====================   =========================================================
        '''
        QtGui.QDialog.__init__(self)
        self._wantToClose = False
        self.unpackDict = unpackDict

        if stayOpen:
            self.finished.connect(self.stayOpen)

        self.setWindowTitle(title)
        layout = QtGui.QGridLayout()
        self.setLayout(layout)

        if introduction:
            pass

        self.values = []
        self.args = {}

        for row, (name, val) in enumerate(argdict.iteritems()):
            limits = val.get('limits', None)
            value = str(val.get('value', ''))
            unit = val.get('unit', None)
            dtype = val.get('dtype', None)
            tip = val.get('tip', None)

            # NAME
            nameLabel = QtGui.QLabel(name)
            layout.addWidget(nameLabel, row, 0)
                # LINE
            if dtype == 'line':
                nameLabel.setText('<b>%s</b>' %nameLabel.text())
                line = QtGui.QFrame()
                line.setFrameStyle(QtGui.QFrame.HLine | QtGui.QFrame.Raised)
                layout.addWidget(line, row, 1, 1, 3)
                # FILE/DIRECTORY
            elif dtype in (file, dir):
                wl = QtGui.QHBoxLayout()
                q = QtGui.QLineEdit(value)
                btn = QtGui.QPushButton()

                if dtype == file:
                    fn = self._getFile
                    btn.setIcon(QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_FileIcon))

                else:
                    fn = self._getFolder
                    btn.setIcon(QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_DirIcon))

                btn.clicked.connect(lambda checked, fn=fn, lineEdit=q: fn(lineEdit))

                wl.addWidget(q)
                wl.addWidget(btn)
                layout.addLayout(wl, row, 1)

                self.values.append((name, q, str))
                # STR/INT,BOOL, FLOAT
            else:
                if type(limits) in (list, tuple):
                    # create a QCombobox if LIMITS are given
                    q = QtGui.QComboBox()
                    q.text = q.currentText
                    for n, l in enumerate(limits):
                        limits[n] = str(l)
                    if value:
                        if value in limits:
                            limits.remove(value)
                        limits.insert(0,value)
                    q.addItems(limits)
                else:
                    # if NO LIMITS given: create a lieEdit 
                    q = QtGui.QLineEdit(value)
                    if dtype and dtype in self.validators:
                        q.setValidator(self.validators[dtype]())
                if tip:
                    q.setToolTip(tip)
                # VALUE
                layout.addWidget(q, row, 1)
                # UNIT
                if unit:
                    layout.addWidget(QtGui.QLabel(str(unit)), row, 2)

                self.values.append((name, q, dtype))

        # SAVE/LOAD BUTTON
        if saveLoadButton:
            box = QtGui.QGroupBox('Preferences')
            bLayout = QtGui.QGridLayout()
            box.setLayout(bLayout)

            btn_load = QtGui.QPushButton('Load')
            self.label_load = QtGui.QLineEdit(loadPath)
            btn_change_load = QtGui.QPushButton()
            btn_change_load.setIcon(QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_DirIcon))
            btn_change_load.clicked.connect(self._setLoadPath)
            btn_load.clicked.connect(self._loadPreferences)

            btn_save = QtGui.QPushButton('Save')
            self.label_save = QtGui.QLineEdit(savePath)
            btn_change_save = QtGui.QPushButton()
            btn_change_save.setIcon(QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_DirIcon))
            btn_change_save.clicked.connect(self._setSavePath)
            btn_save.clicked.connect(self._savePreferences)

            bLayout.addWidget(btn_load, 0,0)
            bLayout.addWidget(self.label_load, 0,1)
            bLayout.addWidget(btn_change_load, 0,2)
            bLayout.addWidget(btn_save, 1,0)
            bLayout.addWidget(self.label_save, 1,1)
            bLayout.addWidget(btn_change_save, 1,2)

            row += 1
            layout.addWidget(box, row, 0, 1, 3)

        # DONE BUTTON
        self.btn_done = QtGui.QPushButton('done')
        self.btn_done.clicked.connect(self.check)
        layout.addWidget(self.btn_done, row+1,0, 1, 3)


    @staticmethod
    def _getFile(lineEdit):
        filename = QtGui.QFileDialog.getOpenFileName(directory=lineEdit.text())
        if filename:
            lineEdit.setText(str(filename))


    @staticmethod
    def _getFolder(lineEdit):
        folder = QtGui.QFileDialog.getExistingDirectory(directory=lineEdit.text())
        if folder:
            lineEdit.setText(str(folder))


    def _setSavePath(self):
        path = QtGui.QFileDialog.getSaveFileName(filter='*.txt')
        self.label_save.setText(path) 


    def _setLoadPath(self):
        path = QtGui.QFileDialog.getOpenFileName(filter='*.txt')
        self.label_load.setText(path) 


    def _savePreferences(self):
        if self.label_save.text() in ('', '[NOT SAVED]'):
            self._setSavePath()
        if self.label_save.text() == '':
            self.label_save.setText('[NOT SAVED]')
            return
        with open(self.label_save.text(),'w') as f:
            d = {}
            for name, widget, _ in self.values:
                d[name] = unicode(widget.text())
            f.write(str(d))


    def _loadPreferences(self):
        if self.label_load.text() in ('', '[NOT LOADED]'):
            self._setLoadPath()
        if self.label_load.text() == '':
            self.label_load.setText('[NOT LOADED]')
            return
        with open(self.label_load.text(), 'r') as f:
            d = eval(f.read())
            for name, widget, _ in self.values:
                if isinstance(widget, QtGui.QComboBox):
                    for c in range(widget.count()):
                        if widget.itemText(c) == d[name]:
                            widget.setCurrentIndex(c)
                else:
                    widget.setText(d[name])


    def show(self):
        '''
        if the dialog is showed again or is not started with exec_
        naming the done button to 'update' make more sense
        because now the dialog doesn't block (anymore)
        '''
        self.btn_done.clicked.connect(lambda: self.btn_done.setText('update'))
        QtGui.QDialog.show(self)


    def run(self, processClass):
        self.processClass = processClass
        QtGui.QDialog.show(self)
        self.btn_done.clicked.connect(self._startProcess)


    def _startProcess(self):
        self.btn_done.clicked.disconnect(self._startProcess)
        if self.unpackDict:
            p = self.processClass(**self.args)
        else:
            p = self.processClass(self.args)
        self.btn_done.setText('update')


    def check(self):
        '''check whether all attributes are setted and have the right dtype'''
        for name, valItem, dtype in self.values:
            val = valItem.text()
            if dtype:
                try:
                    val = dtype(val)
                except:
                    msgBox = QtGui.QMessageBox()
                    msgBox.setText('attribute %s has not the right dtype(%s)' %(name, str(dtype)))
                    msgBox.exec_()
            self.args[name] = val
        self.accept()


    def closeEvent(self, evt):
        self._wantToClose = True
        QtGui.QDialog.closeEvent(self, evt)


    def done(self, result):
        '''save the geometry before dialog is close to restore it later'''
        self._geometry = self.geometry()
        QtGui.QDialog.done(self, result)


    def stayOpen(self):
        '''optional dialog restore'''
        if not self._wantToClose:
            self.show()
            self.setGeometry(self._geometry)



if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)

    print("""TEST 1:
* ArgSetter will block until the button 'done' is pressed. 
* If the dialog is not cancelled the arguments are printed""")

    a = ArgSetter('CloseAfterDone', {
            'show_output_after_start':{
                            'value': True, 
                            'limits':[True, False], 
                            'dtype':bool,
                            'tip':'foo bar'},
            'webcam_index': {
                            'value':-1,
                            'limits':range(-1,10), 
                            'dtype':int},
            'output_file_name':{
                            'value':'output.csv',
                            'dtype':str},
            'camera_calibration_File':{
                            'value':'', 
                            'dtype':str},
            'nAverageSteps': {
                            'value':3, 
                            'limits':range(1,20), 
                            'dtype':int},
            'refreshRate': {
                            'value':100, 
                            'dtype':int, 
                            'unit':'ms'}
            })

    a.exec_()
    if a.result():
        print a.args
    else:
        print 'setup cancelled'


    print("""TEST 2:
* ArgSetter won't block but update its agument every time 'update' is pressed. """)

    a = ArgSetter('StayOpen', {
            'one':{
                            'value': True, 
                            'limits':[True, False], 
                            'dtype':bool,
                            'tip':'foo bar'},
            'two': {
                            'value':-1, 
                            'limits':range(-1,10), 
                            'dtype':int},
            'three':{
                            'value':'output.csv',
                            'dtype':str},
            'four':{
                            'value':'', 
                            'dtype':str},
            'fife': {
                            'value':3, 
                            'limits':range(1,20), 
                            'dtype':int},
            'six': {
                            'value':100, 
                            'dtype':int, 
                            'unit':'ms'}
            }, stayOpen=True, saveLoadButton=True)


    class MyProcedure(QtGui.QTextEdit):
        '''
        a procedure taking the argument from ArgSetter
        as self.opts

        This shows the feature to interactively update argument using a
        graphical interface
        '''

        def __init__(self, opts):
            QtGui.QWidget.__init__(self)
            self.setReadOnly(True)
            self.opts = opts
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(lambda: self.setText(str(self.opts)))
            self.timer.start(100)
            self.show()
    a.run(MyProcedure)

    app.exec_()

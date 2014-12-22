
from PyQt4 import QtGui, QtCore


class ArgSetter(QtGui.QDialog):
    '''
    create an window to setup attributes graphically needed by 
    other functions/classes
    
    useful as quick configurator for other functions/classes that need 
    keyword arguments that must be passed graphically 
    e.g. for py2exe/pyinstaller apps
    '''
    validators = {float:QtGui.QDoubleValidator, 
                  int:QtGui.QIntValidator}
    def __init__(self, title, argdict, stayOpen=False):
        '''
        =========   ================================================================
        Argument    Comment
        =========   ================================================================
        title       title of the window
        argdict     a dict of all arguments to set up:
                    e.g. {'arg1: {'value':1, 'limits':range(0,10)}, ...}
                    valid keywords are:
                         'value' -> the value of the argument
                         'limits' -> [list, tuple] if only specific values are valid
                         'unit' -> show a unit after the value
                         'tip' -> show a tooltip
                         'dtype' -> the datatype of the value
        stayOpen    'True' -> dialog stays open after it is finished
                    useful if values should still be changeable
        =========   ================================================================      
        '''
        QtGui.QDialog.__init__(self)
        self._wantToClose = False
        if stayOpen:
            self.finished.connect(self.stayOpen)
        
        self.setWindowTitle(title)
        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)
        
        self.values = []
        self.args = {}
        
        for name, val in argdict.iteritems():

            limits = val.get('limits', None)
            value = str(val.get('value', ''))
            unit = val.get('unit', None)
            dtype = val.get('dtype', None)
            tip = val.get('tip', None)
            
            rowlayout = QtGui.QHBoxLayout()
            layout.addLayout(rowlayout)
            #NAME
            rowlayout.addWidget(QtGui.QLabel(name))
            
            if type(limits) in (list, tuple):
                # create a QCombobox if LIMITS are given
                q = QtGui.QComboBox()
                q.text = q.currentText
                for n,l in enumerate(limits):
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
            rowlayout.addWidget(q)
            #UNIT
            if unit:
                rowlayout.addWidget(QtGui.QLabel(str(unit)))
                
            self.values.append((name, q, dtype))
                
        self.btn_done = QtGui.QPushButton('done')
        self.btn_done.clicked.connect(self.check)
        layout.addWidget(self.btn_done)


    def show(self):
        '''
        if the dialog is showed again or is not started with exec_
        naming the done button to 'update' make more sense
        because now the dialog doesn't block (anymore)
        ''' 
        self.btn_done.setText('update')
        QtGui.QDialog.show(self)
        

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
            }, stayOpen=True)
    
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
            }, stayOpen=True)


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
            
    a.show()
    m = MyProcedure(a.args)
    m.show()


    app.exec_()

    
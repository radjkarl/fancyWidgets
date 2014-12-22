#!/usr/bin/env python


if __name__ == '__main__':
    import sys
    import os
    
    from PyQt4 import QtCore, QtGui
    ##
    # Tell Qt Designer where it can find the directory containing the plugins and
    # Python where it can find the widgets.
    env = os.environ.copy()
    import fwQtDesigner_plugins 
    env['PYQTDESIGNERPATH'] = os.path.dirname(fwQtDesigner_plugins.__file__)
    
    app = QtGui.QApplication(sys.argv)
    
    qenv = ['%s=%s' % (name, value) for name, value in env.items()]
    
    # Start Designer.
    designer = QtCore.QProcess()
    designer.setEnvironment(qenv)
    
    designer_bin = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.BinariesPath)
    
    if sys.platform == 'darwin':
        designer_bin += '/Designer.app/Contents/MacOS/Designer'
    else:
        designer_bin += '/designer'
    
    designer.start(designer_bin)
    designer.waitForFinished(-1)
    
    sys.exit(designer.exitCode())

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
#     env['PYTHONPATH'] = 'widgets' 
    
    app = QtGui.QApplication(sys.argv)
    
#     QtGui.QMessageBox.information(None, "PyQt Designer Plugins",
#             "<p>This example will start Qt Designer when you click the <b>OK</b> "
#             "button.</p>"
#             "<p>Before doing so it sets the <tt>PYQTDESIGNERPATH</tt> environment "
#             "variable to the <tt>python</tt> directory that is part of this "
#             "example.  This directory contains all the example Python plugin "
#             "modules.</p>"
#             "<p>It also sets the <tt>PYTHONPATH</tt> environment variable to the "
#             "<tt>widgets</tt> directory that is also part of this example.  This "
#             "directory contains the Python modules that implement the example "
#             "custom widgets.</p>"
#             "<p>All of the example custom widgets should then appear in "
#             "Designer's widget box in the <b>PyQt Examples</b> group.</p>")
    

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

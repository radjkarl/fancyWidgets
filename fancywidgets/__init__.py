__all__ = ['FwImageView', 'FwMinimalTextEditor', 'FwTabWidget', 'FwTextEditor', '_dialogs', '_textEditorUtils', 'dock', 'dockArea', 'messageDock', 'table', 'ImageExporter', 'pgImageView', 'Qt', 'ToolBarFont', 'ToolBarFormat', 'ToolBarEdit', 'PathStr', 'getExistingDirectory', 'getOpenFileName', 'getSaveFileName', 'Date', 'Find', 'Dock', 'DockLabelMenu', 'pgDockDrop', 'pgDockLabel', 'DockArea', 'QWidget', 'l', 'pgDockArea', 'MessageDock', 'StreamSignal', 'Table', '_Header', '_HeaderMenu', '_TableMenu']
# Don't modify the line above, or this line!


__version__ = '0.1.0'
__author__ = 'Karl Bedrich'
__email__ = 'karl@bedrich.de'
__url__ = 'http://pypi.python.org/pypi/fancyWidgets/'
__license__ = 'GPLv3'
__description__ = '...'#TODO
__depencies__= [
                #PyQt4,
        "fancytools",
      #  "ordereddict >= 1.1",
      #  "numpy >= 1.7.1",
        "autoxinit >= 0.1.0"
    ]
__classifiers__ = [
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]


# This module is also imported for installing the package
# Load only the second part of the init if this package is installed and
# all depencies are fulfilled
import sys
if sys.modules['fancywidgets']:
    try:
        import autoxinit
        autoxinit.autoxinit(__name__, __file__, globals())
        del autoxinit
        # Anything else you want can go after here, it won't get modified.
    except ImportError:
        pass
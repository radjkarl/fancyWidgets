# coding=utf-8
"""A vertical tab widget - code origin from:
https://gist.github.com/LegoStormtroopr/5075267
"""
from qtpy import QtWidgets, QtCore


class FingerTabBarWidget(QtWidgets.QTabBar):

    def __init__(self, parent=None, *args, **kwargs):
        self.tabSize = QtCore.QSize(
            kwargs.pop(
                'width', 100), kwargs.pop(
                'height', 25))
        QtWidgets.QTabBar.__init__(self, parent, *args, **kwargs)

    def paintEvent(self, event):
        painter = QtWidgets.QStylePainter(self)
        option = QtWidgets.QStyleOptionTab()

        for index in range(self.count()):
            self.initStyleOption(option, index)
            tabRect = self.tabRect(index)
            tabRect.moveLeft(10)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabShape, option)
            painter.drawText(tabRect, QtCore.Qt.AlignVCenter |
                             QtCore.Qt.TextDontClip,
                             self.tabText(index))
        painter.end()

    def tabSizeHint(self, index):
        return self.tabSize


# Shamelessly stolen from this thread:
#   http://www.riverbankcomputing.com/pipermail/pyqt/2005-December/011724.html
class FingerTabWidget(QtWidgets.QTabWidget):
    """
    A QTabWidget equivalent which uses our FingerTabBarWidget
    """

    def __init__(self, parent=None, *args, **kwargs):
        pos = kwargs.pop('pos', QtWidgets.QTabWidget.West)

        QtWidgets.QTabWidget.__init__(self, parent, *args, **kwargs)
        self.setTabBar(FingerTabBarWidget(self))

        self.setTabPosition(pos)


class AutoResizeFingerTabWidget(FingerTabWidget):

    def __init__(self, parent=None, *args, **kwargs):
        FingerTabWidget.__init__(self, parent, *args, **kwargs)
        if parent is not None:
            parent.resizeEvent = self.forceResize

    def forceResize(self, evt):
        self.setFixedSize(evt.size())


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # with default opts:
    w = FingerTabWidget()
    w.setWindowTitle(w.__class__.__name__)

    # with individual opts
    w2 = FingerTabWidget(width=200, height=500, pos=QtWidgets.QTabWidget.East)
    w2.setWindowTitle(w.__class__.__name__)

    digits = ['Thumb', 'Pointer', 'Rude', 'Ring', 'Pinky']
    for i, d in enumerate(digits):
        widget = QtWidgets.QLabel("Area #%s <br> %s Finger" % (i, d))
        widget2 = QtWidgets.QLabel("Area #%s <br> %s Finger" % (i, d))
        w.addTab(widget, d)
        w2.addTab(widget2, d)

    w.show()
    w2.show()

    app.exec_()
